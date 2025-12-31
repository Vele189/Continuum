"""
HMAC verification utilities for webhook security.

Provides secure HMAC SHA-256 signature verification for GitHub and Bitbucket webhooks.
Uses hmac.compare_digest to prevent timing attacks.
"""

import hashlib
import hmac
from typing import Optional

from app.utils.logger import get_logger

logger = get_logger(__name__)


def verify_github_signature(
    payload_body: bytes, signature_header: Optional[str], secret: str
) -> bool:
    """
    Verify GitHub webhook signature using HMAC SHA-256.

    GitHub sends the signature in the format: sha256=<hex_digest>
    The signature is computed over the raw request body.

    Args:
        payload_body: Raw request body bytes
        signature_header: X-Hub-Signature-256 header value (format: sha256=<hex>)
        secret: Webhook secret configured in GitHub

    Returns:
        True if signature is valid, False otherwise
    """
    if not signature_header:
        logger.warning("GitHub webhook missing signature header")
        return False

    if not secret:
        logger.error("GitHub webhook secret not configured")
        return False

    try:
        # GitHub sends: sha256=<hex_digest>
        if not signature_header.startswith("sha256="):
            logger.warning("GitHub signature header has invalid format")
            return False

        expected_signature = signature_header[7:]  # Remove "sha256=" prefix

        # Compute HMAC SHA-256
        computed_signature = hmac.new(
            secret.encode("utf-8"), payload_body, hashlib.sha256
        ).hexdigest()

        # Use compare_digest to prevent timing attacks
        return hmac.compare_digest(computed_signature, expected_signature)

    except Exception as e:
        logger.error("Error verifying GitHub signature: %s", e, exc_info=True)
        return False


def verify_bitbucket_signature(
    payload_body: bytes, signature_header: Optional[str], secret: str
) -> bool:
    """
    Verify Bitbucket webhook signature using HMAC SHA-256.

    Bitbucket sends the signature in the X-Hub-Signature header.
    The signature is computed over the raw request body.

    Args:
        payload_body: Raw request body bytes
        signature_header: X-Hub-Signature header value
        secret: Webhook secret configured in Bitbucket

    Returns:
        True if signature is valid, False otherwise
    """
    if not signature_header:
        logger.warning("Bitbucket webhook missing signature header")
        return False

    if not secret:
        logger.error("Bitbucket webhook secret not configured")
        return False

    try:
        # Bitbucket sends the raw hex digest (no prefix)
        expected_signature = signature_header

        # Compute HMAC SHA-256
        computed_signature = hmac.new(
            secret.encode("utf-8"), payload_body, hashlib.sha256
        ).hexdigest()

        # Use compare_digest to prevent timing attacks
        return hmac.compare_digest(computed_signature, expected_signature)

    except Exception as e:
        logger.error("Error verifying Bitbucket signature: %s", e, exc_info=True)
        return False
