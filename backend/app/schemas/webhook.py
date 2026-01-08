"""
Webhook payload schemas for Git providers.

These schemas validate the structure of incoming webhook payloads
from GitHub, GitLab, and Bitbucket.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


# Common schemas
class CommitAuthor(BaseModel):
    """Commit author information."""

    name: str
    email: str


class CommitInfo(BaseModel):
    """Standardized commit information."""

    hash: str
    message: str
    branch: str
    timestamp: datetime
    author_email: str
    author_name: str
    url: Optional[str] = None


# GitHub schemas
class GitHubCommit(BaseModel):
    """GitHub commit object."""

    id: str = Field(alias="sha")
    message: str
    author: Optional[Dict[str, Any]] = None
    committer: Optional[Dict[str, Any]] = None
    url: Optional[str] = None
    timestamp: Optional[str] = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, v):
        """Ensure commit hash is provided."""
        if not v or not v.strip():
            raise ValueError("Commit SHA is required")
        return v.strip()


class GitHubPushPayload(BaseModel):
    """GitHub push event payload."""

    ref: str  # e.g., "refs/heads/main"
    commits: List[GitHubCommit]
    repository: Dict[str, Any]
    pusher: Optional[Dict[str, Any]] = None

    @field_validator("ref")
    @classmethod
    def validate_ref(cls, v):
        """Ensure ref is provided."""
        if not v:
            raise ValueError("Ref is required")
        return v


# GitLab schemas
class GitLabCommit(BaseModel):
    """GitLab commit object."""

    id: str
    message: str
    author_name: str
    author_email: str
    timestamp: str
    url: Optional[str] = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, v):
        """Ensure commit hash is provided."""
        if not v or not v.strip():
            raise ValueError("Commit ID is required")
        return v.strip()


class GitLabPushPayload(BaseModel):
    """GitLab push event payload."""

    ref: str  # e.g., "refs/heads/main"
    commits: List[GitLabCommit]
    project: Optional[Dict[str, Any]] = None
    repository: Optional[Dict[str, Any]] = None

    @field_validator("ref")
    @classmethod
    def validate_ref(cls, v):
        """Ensure ref is provided."""
        if not v:
            raise ValueError("Ref is required")
        return v


# Bitbucket schemas
class BitbucketCommit(BaseModel):
    """Bitbucket commit object."""

    hash: str
    message: str
    author: Optional[Dict[str, Any]] = None
    date: Optional[str] = None

    @field_validator("hash")
    @classmethod
    def validate_hash(cls, v):
        """Ensure commit hash is provided."""
        if not v or not v.strip():
            raise ValueError("Commit hash is required")
        return v.strip()


class BitbucketPushPayload(BaseModel):
    """Bitbucket push event payload."""

    push: Optional[Dict[str, Any]] = None
    repository: Optional[Dict[str, Any]] = None

    def get_commits(self) -> List[Dict[str, Any]]:
        """Extract commits from Bitbucket push payload."""
        if not self.push:
            return []
        changes = self.push.get("changes", [])
        commits = []
        for change in changes:
            if "commits" in change.get("new", {}):
                commits.extend(change["new"]["commits"])
        return commits

    def get_branch(self) -> Optional[str]:
        """Extract branch name from Bitbucket push payload."""
        if not self.push:
            return None
        changes = self.push.get("changes", [])
        if changes and "new" in changes[0]:
            return changes[0]["new"].get("name")
        return None
