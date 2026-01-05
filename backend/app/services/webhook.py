"""
Webhook processing service for Git providers.

Handles extraction, normalization, and persistence of commits from
GitHub, GitLab, and Bitbucket webhook payloads.
"""

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.dbmodels import GitContribution, Project, User
from app.schemas.webhook import (
    BitbucketPushPayload,
    CommitInfo,
    GitHubPushPayload,
    GitLabPushPayload,
)
from app.utils.logger import get_logger
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

logger = get_logger(__name__)


# Common no-reply email patterns
NO_REPLY_PATTERNS = [
    r"noreply@.*",
    r"no-reply@.*",
    r".*@users\.noreply\.github\.com",
    r".*@users\.noreply\.gitlab\.com",
    r".*@bitbucket\.org",
]


class WebhookService:
    """Service for processing Git webhook payloads."""

    @staticmethod
    def _is_no_reply_email(email: str) -> bool:
        """
        Check if an email is a no-reply address.

        Args:
            email: Email address to check

        Returns:
            True if email matches no-reply patterns, False otherwise
        """
        if not email:
            return True

        email_lower = email.lower().strip()
        for pattern in NO_REPLY_PATTERNS:
            if re.match(pattern, email_lower):
                logger.debug("Ignoring no-reply email: %s", email)
                return True
        return False

    @staticmethod
    def _normalize_timestamp(timestamp_str: str, provider: str) -> datetime:
        """
        Normalize timestamp string to timezone-aware datetime.

        Args:
            timestamp_str: Timestamp string from webhook
            provider: Provider name (github, gitlab, bitbucket)

        Returns:
            Timezone-aware datetime object
        """
        try:
            # Try parsing ISO format (most common)
            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                # If no timezone info, assume UTC
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except (ValueError, AttributeError):
            # Fallback: try common formats
            formats = [
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d %H:%M:%S%z",
            ]
            for fmt in formats:
                try:
                    dt = datetime.strptime(timestamp_str, fmt)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt
                except ValueError:
                    continue

            # Last resort: use current time
            logger.warning(
                "Could not parse timestamp '%s' from %s, using current time",
                timestamp_str,
                provider,
            )
            return datetime.now(timezone.utc)

    @staticmethod
    def _extract_branch_from_ref(ref: str) -> str:
        """
        Extract branch name from Git ref.

        Args:
            ref: Git ref (e.g., "refs/heads/main")

        Returns:
            Branch name (e.g., "main")
        """
        if ref.startswith("refs/heads/"):
            return ref[11:]
        if ref.startswith("refs/"):
            return ref[5:]
        return ref

    @staticmethod
    def _find_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Find user by email (case-insensitive).

        Args:
            db: Database session
            email: Email address to search for

        Returns:
            User if found, None otherwise
        """
        if not email:
            return None

        # Case-insensitive search
        user = db.query(User).filter(User.email.ilike(email.strip())).first()

        return user

    @staticmethod
    def _get_project_by_repository(
        _db: Session, repository_url: str, repository_name: str
    ) -> Optional[Project]:
        """
        Get project by repository URL or name.

        TODO: This is a placeholder. Repository → Project mapping
        will be implemented in a follow-up ticket.

        Args:
            _db: Database session (unused for now)
            repository_url: Repository URL from webhook
            repository_name: Repository name from webhook

        Returns:
            Project if mapping exists, None otherwise
        """
        # For now, return None to enforce blocking behavior
        # This will be implemented in a follow-up ticket
        logger.debug(
            "Repository mapping not yet implemented. URL: %s, Name: %s",
            repository_url,
            repository_name,
        )

    @staticmethod
    def _extract_github_commits(payload: GitHubPushPayload) -> List[CommitInfo]:
        """
        Extract and normalize commits from GitHub push payload.

        Args:
            payload: GitHub push event payload

        Returns:
            List of normalized commit information
        """
        commits = []
        branch = WebhookService._extract_branch_from_ref(payload.ref)

        for commit in payload.commits:
            # Extract author email (prefer author over committer)
            author_email = None
            author_name = None

            if commit.author:
                author_email = commit.author.get("email")
                author_name = commit.author.get("name")

            if not author_email and commit.committer:
                author_email = commit.committer.get("email")
                author_name = commit.committer.get("name")

            # Extract timestamp
            timestamp_str = commit.timestamp
            if not timestamp_str and commit.author:
                timestamp_str = commit.author.get("date")
            if not timestamp_str and commit.committer:
                timestamp_str = commit.committer.get("date")

            if not timestamp_str:
                timestamp_str = datetime.now(timezone.utc).isoformat()

            commits.append(
                CommitInfo(
                    hash=commit.id,
                    message=commit.message or "",
                    branch=branch,
                    timestamp=WebhookService._normalize_timestamp(timestamp_str, "github"),
                    author_email=author_email or "",
                    author_name=author_name or "",
                    url=commit.url,
                )
            )

        return commits

    @staticmethod
    def _extract_gitlab_commits(payload: GitLabPushPayload) -> List[CommitInfo]:
        """
        Extract and normalize commits from GitLab push payload.

        Args:
            payload: GitLab push event payload

        Returns:
            List of normalized commit information
        """
        commits = []
        branch = WebhookService._extract_branch_from_ref(payload.ref)

        for commit in payload.commits:
            commits.append(
                CommitInfo(
                    hash=commit.id,
                    message=commit.message or "",
                    branch=branch,
                    timestamp=WebhookService._normalize_timestamp(commit.timestamp, "gitlab"),
                    author_email=commit.author_email or "",
                    author_name=commit.author_name or "",
                    url=commit.url,
                )
            )

        return commits

    @staticmethod
    def _extract_bitbucket_commits(payload: BitbucketPushPayload) -> List[CommitInfo]:
        """
        Extract and normalize commits from Bitbucket push payload.

        Args:
            payload: Bitbucket push event payload

        Returns:
            List of normalized commit information
        """
        commits = []
        branch = payload.get_branch()
        if not branch:
            logger.warning("Could not extract branch from Bitbucket payload")
            return commits

        commit_data_list = payload.get_commits()
        for commit_data in commit_data_list:
            # Skip if hash is missing
            commit_hash = commit_data.get("hash", "").strip()
            if not commit_hash:
                logger.warning("Skipping commit with missing hash in Bitbucket payload")
                continue

            # Extract author information
            author = commit_data.get("author", {})
            author_email = ""
            author_name = ""

            if isinstance(author, dict):
                # Try to extract from raw field (format: "Name <email@example.com>")
                if "raw" in author:
                    raw_str = author["raw"]
                    if "<" in raw_str and ">" in raw_str:
                        author_name = raw_str.split("<")[0].strip()
                        author_email = raw_str.split("<")[-1].split(">")[0].strip()
                    else:
                        author_name = raw_str.strip()
                # Fallback to user object
                if not author_email:
                    user = author.get("user", {})
                    if isinstance(user, dict):
                        author_email = user.get("email_address", "") or user.get("email", "")
                        author_name = user.get("display_name", "") or user.get("display_name", "")

            # Extract timestamp
            timestamp_str = commit_data.get("date") or commit_data.get("timestamp", "")

            if not timestamp_str:
                timestamp_str = datetime.now(timezone.utc).isoformat()

            commits.append(
                CommitInfo(
                    hash=commit_hash,
                    message=commit_data.get("message", ""),
                    branch=branch,
                    timestamp=WebhookService._normalize_timestamp(timestamp_str, "bitbucket"),
                    author_email=author_email or "",
                    author_name=author_name or "",
                    url=None,  # Bitbucket doesn't provide commit URL in push payload
                )
            )

        return commits

    @staticmethod
    def process_github_push(
        db: Session,
        payload: GitHubPushPayload,
        repository_url: Optional[str] = None,
        repository_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process GitHub push event and create contributions.

        Args:
            db: Database session
            payload: GitHub push event payload
            repository_url: Repository URL (from payload.repository.clone_url or similar)
            repository_name: Repository name (from payload.repository.full_name or similar)

        Returns:
            Dictionary with processing results
        """
        logger.info("Processing GitHub push event")

        # Extract repository info if not provided
        if not repository_url and payload.repository:
            repository_url = payload.repository.get("clone_url") or payload.repository.get(
                "html_url"
            )
        if not repository_name and payload.repository:
            repository_name = payload.repository.get("full_name") or payload.repository.get("name")

        # Check project mapping
        project = WebhookService._get_project_by_repository(
            db, repository_url or "", repository_name or ""
        )

        if not project:
            logger.warning(
                "No project mapping found for repository: %s", repository_name or repository_url
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project mapping required. Repository not linked to a project.",
            )

        # Extract commits
        commits = WebhookService._extract_github_commits(payload)
        logger.info("Extracted %d commits from GitHub push", len(commits))

        # Process commits
        return WebhookService._process_commits(db, commits, project.id, "github", repository_url)

    @staticmethod
    def process_gitlab_push(
        db: Session,
        payload: GitLabPushPayload,
        repository_url: Optional[str] = None,
        repository_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process GitLab push event and create contributions.

        Args:
            db: Database session
            payload: GitLab push event payload
            repository_url: Repository URL (from payload.repository.git_http_url or similar)
            repository_name: Repository name (from payload.project.path_with_namespace or similar)

        Returns:
            Dictionary with processing results
        """
        logger.info("Processing GitLab push event")

        # Extract repository info if not provided
        if not repository_url and payload.repository:
            repository_url = payload.repository.get("git_http_url") or payload.repository.get("url")
        if not repository_name and payload.project:
            repository_name = payload.project.get("path_with_namespace") or payload.project.get(
                "name"
            )

        # Check project mapping
        project = WebhookService._get_project_by_repository(
            db, repository_url or "", repository_name or ""
        )

        if not project:
            logger.warning(
                "No project mapping found for repository: %s", repository_name or repository_url
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project mapping required. Repository not linked to a project.",
            )

        # Extract commits
        commits = WebhookService._extract_gitlab_commits(payload)
        logger.info("Extracted %d commits from GitLab push", len(commits))

        # Process commits
        return WebhookService._process_commits(db, commits, project.id, "gitlab", repository_url)

    @staticmethod
    def process_bitbucket_push(
        db: Session,
        payload: BitbucketPushPayload,
        repository_url: Optional[str] = None,
        repository_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process Bitbucket push event and create contributions.

        Args:
            db: Database session
            payload: Bitbucket push event payload
            repository_url: Repository URL (from payload.repository.links.html.href or similar)
            repository_name: Repository name (from payload.repository.full_name or similar)

        Returns:
            Dictionary with processing results
        """
        logger.info("Processing Bitbucket push event")

        # Extract repository info if not provided
        if not repository_url and payload.repository:
            repo = payload.repository
            if isinstance(repo, dict):
                links = repo.get("links", {})
                if isinstance(links, dict):
                    html_link = links.get("html", {})
                    if isinstance(html_link, dict):
                        repository_url = html_link.get("href")

        if not repository_name and payload.repository:
            repo = payload.repository
            if isinstance(repo, dict):
                repository_name = repo.get("full_name") or repo.get("name")

        # Check project mapping
        project = WebhookService._get_project_by_repository(
            db, repository_url or "", repository_name or ""
        )

        if not project:
            logger.warning(
                "No project mapping found for repository: %s", repository_name or repository_url
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project mapping required. Repository not linked to a project.",
            )

        # Extract commits
        commits = WebhookService._extract_bitbucket_commits(payload)
        logger.info("Extracted %d commits from Bitbucket push", len(commits))

        # Process commits
        return WebhookService._process_commits(db, commits, project.id, "bitbucket", repository_url)

    @staticmethod
    def _process_commits(
        db: Session,
        commits: List[CommitInfo],
        project_id: int,
        provider: str,
        repository_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process commits and create contributions.

        Args:
            db: Database session
            commits: List of normalized commit information
            project_id: Project ID to associate commits with
            provider: Provider name (github, gitlab, bitbucket)
            repository_url: Repository URL for building commit URLs

        Returns:
            Dictionary with processing statistics
        """
        created_count = 0
        skipped_count = 0
        no_user_count = 0
        no_reply_count = 0

        for commit in commits:
            try:
                # Skip no-reply emails
                if WebhookService._is_no_reply_email(commit.author_email):
                    logger.debug(
                        "Skipping commit %s: no-reply email %s",
                        commit.hash[:8],
                        commit.author_email,
                    )
                    no_reply_count += 1
                    continue

                # Find user by email
                user = WebhookService._find_user_by_email(db, commit.author_email)

                if not user:
                    logger.debug(
                        "Skipping commit %s: no user found for email %s",
                        commit.hash[:8],
                        commit.author_email,
                    )
                    no_user_count += 1
                    continue

                # Check for duplicate
                existing = (
                    db.query(GitContribution)
                    .filter(
                        GitContribution.project_id == project_id,
                        GitContribution.commit_hash == commit.hash,
                    )
                    .first()
                )

                if existing:
                    logger.debug("Skipping duplicate commit %s (already exists)", commit.hash[:8])
                    skipped_count += 1
                    continue

                # Build commit URL if not provided
                commit_url = commit.url
                if not commit_url and repository_url:
                    # Try to construct URL based on provider
                    if provider == "github":
                        commit_url = f"{repository_url}/commit/{commit.hash}"
                    elif provider == "gitlab":
                        commit_url = f"{repository_url}/-/commit/{commit.hash}"
                    elif provider == "bitbucket":
                        commit_url = f"{repository_url}/commits/{commit.hash}"

                # Create contribution
                contribution = GitContribution(
                    user_id=user.id,
                    project_id=project_id,
                    commit_hash=commit.hash,
                    branch=commit.branch,
                    commit_message=commit.message,
                    provider=provider,
                    commit_url=commit_url,
                    committed_at=commit.timestamp,
                )

                db.add(contribution)
                created_count += 1
                logger.info(
                    "Created contribution for commit %s (user: %s, project: %d)",
                    commit.hash[:8],
                    user.email,
                    project_id,
                )

            except Exception as e:
                logger.error(
                    "Error processing commit %s: %s",
                    commit.hash[:8] if commit else "unknown",
                    e,
                    exc_info=True,
                )
                # Continue processing other commits
                continue

        # Commit all changes
        try:
            db.commit()
            logger.info(
                "Webhook processing complete: %d created, %d skipped (duplicates), "
                "%d skipped (no user), %d skipped (no-reply)",
                created_count,
                skipped_count,
                no_user_count,
                no_reply_count,
            )
        except Exception as e:
            db.rollback()
            logger.error("Error committing contributions: %s", e, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to persist contributions",
            ) from e

        return {
            "created": created_count,
            "skipped_duplicates": skipped_count,
            "skipped_no_user": no_user_count,
            "skipped_no_reply": no_reply_count,
            "total_processed": len(commits),
        }
