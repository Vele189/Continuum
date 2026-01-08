"""
Webhook endpoints for Git providers.

Handles incoming webhook events from GitHub, GitLab, and Bitbucket,
verifies their authenticity, and processes push events to track contributions.
"""

import hmac
import json
from typing import Any, Dict

from app.api.deps import get_db
from app.core.config import settings
from app.schemas.webhook import BitbucketPushPayload, GitHubPushPayload, GitLabPushPayload
from app.services.webhook import WebhookService
from app.utils.hmac_verifier import verify_bitbucket_signature, verify_github_signature
from app.utils.logger import get_logger
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

logger = get_logger(__name__)

router = APIRouter()


@router.post("/github")
async def github_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_hub_signature_256: str = Header(None, alias="X-Hub-Signature-256"),
    x_github_event: str = Header(None, alias="X-GitHub-Event"),
) -> Dict[str, Any]:
    """
    GitHub webhook endpoint.

    Processes push events from GitHub repositories.
    - Verifies HMAC SHA-256 signature
    - Only processes push events
    - Extracts commits and creates contributions

    Headers:
        X-Hub-Signature-256: HMAC SHA-256 signature (required)
        X-GitHub-Event: Event type (must be 'push')

    Returns:
        Processing results with statistics
    """
    logger.info("Received GitHub webhook request")

    # Check event type
    if x_github_event != "push":
        logger.info("Ignoring non-push event: %s", x_github_event)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Event ignored (not a push event)"}
        )

    # Read raw body for signature verification
    try:
        body_bytes = await request.body()
    except Exception as e:
        logger.error("Error reading request body: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to read request body"
        ) from e

    # Verify signature
    if not verify_github_signature(body_bytes, x_hub_signature_256, settings.GITHUB_WEBHOOK_SECRET):
        logger.warning("GitHub webhook signature verification failed")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    logger.info("GitHub webhook signature verified")

    # Parse and validate payload
    try:
        payload_dict = json.loads(body_bytes.decode("utf-8"))
        payload = GitHubPushPayload(**payload_dict)
    except Exception as e:
        logger.error("Error parsing GitHub payload: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid payload structure: {str(e)}"
        ) from e

    # Process push event
    try:
        result = WebhookService.process_github_push(db, payload)
        logger.info("GitHub webhook processed successfully: %s", result)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error processing GitHub webhook: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process webhook"
        ) from e


@router.post("/gitlab")
async def gitlab_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_gitlab_token: str = Header(None, alias="X-Gitlab-Token"),
    x_gitlab_event: str = Header(None, alias="X-Gitlab-Event"),
) -> Dict[str, Any]:
    """
    GitLab webhook endpoint.

    Processes push events from GitLab repositories.
    - Verifies token authentication
    - Only processes push events
    - Extracts commits and creates contributions

    Headers:
        X-Gitlab-Token: Webhook token (required)
        X-Gitlab-Event: Event type (must be 'Push Hook')

    Returns:
        Processing results with statistics
    """
    logger.info("Received GitLab webhook request")

    # Check event type
    if x_gitlab_event != "Push Hook":
        logger.info("Ignoring non-push event: %s", x_gitlab_event)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Event ignored (not a push event)"}
        )

    # Verify token
    if not settings.GITLAB_WEBHOOK_TOKEN:
        logger.error("GitLab webhook token not configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Webhook token not configured"
        )

    if not x_gitlab_token:
        logger.warning("GitLab webhook missing token header")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    # Use hmac.compare_digest for secure token comparison
    if not hmac.compare_digest(x_gitlab_token, settings.GITLAB_WEBHOOK_TOKEN):
        logger.warning("GitLab webhook token verification failed")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    logger.info("GitLab webhook token verified")

    # Read and parse payload
    try:
        body_bytes = await request.body()
        payload_dict = json.loads(body_bytes.decode("utf-8"))
        payload = GitLabPushPayload(**payload_dict)
    except Exception as e:
        logger.error("Error parsing GitLab payload: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid payload structure: {str(e)}"
        ) from e

    # Process push event
    try:
        result = WebhookService.process_gitlab_push(db, payload)
        logger.info("GitLab webhook processed successfully: %s", result)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error processing GitLab webhook: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process webhook"
        ) from e


@router.post("/bitbucket")
async def bitbucket_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_hub_signature: str = Header(None, alias="X-Hub-Signature"),
    x_event_key: str = Header(None, alias="X-Event-Key"),
) -> Dict[str, Any]:
    """
    Bitbucket webhook endpoint.

    Processes push events from Bitbucket repositories.
    - Verifies HMAC SHA-256 signature
    - Only processes push events
    - Extracts commits and creates contributions

    Headers:
        X-Hub-Signature: HMAC SHA-256 signature (required)
        X-Event-Key: Event type (must be 'repo:push')

    Returns:
        Processing results with statistics
    """
    logger.info("Received Bitbucket webhook request")

    # Check event type
    if x_event_key != "repo:push":
        logger.info("Ignoring non-push event: %s", x_event_key)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Event ignored (not a push event)"}
        )

    # Read raw body for signature verification
    try:
        body_bytes = await request.body()
    except Exception as e:
        logger.error("Error reading request body: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to read request body"
        ) from e

    # Verify signature
    if not verify_bitbucket_signature(
        body_bytes, x_hub_signature, settings.BITBUCKET_WEBHOOK_SECRET
    ):
        logger.warning("Bitbucket webhook signature verification failed")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    logger.info("Bitbucket webhook signature verified")

    # Parse and validate payload
    try:
        payload_dict = json.loads(body_bytes.decode("utf-8"))
        payload = BitbucketPushPayload(**payload_dict)
    except Exception as e:
        logger.error("Error parsing Bitbucket payload: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid payload structure: {str(e)}"
        ) from e

    # Process push event
    try:
        result = WebhookService.process_bitbucket_push(db, payload)
        logger.info("Bitbucket webhook processed successfully: %s", result)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error processing Bitbucket webhook: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process webhook"
        ) from e
