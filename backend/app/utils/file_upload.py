"""
File upload utility with storage abstraction.

This module provides file handling functionality that is storage-agnostic,
allowing for easy migration to S3 or other cloud storage in the future.
"""

import os
import uuid
from pathlib import Path
from typing import Optional

from app.core.config import settings
from fastapi import HTTPException, UploadFile, status


class StorageBackend:
    """Abstract base class for storage backends"""

    def save_file(self, file_content: bytes, file_path: str) -> str:
        """
        Save file content to storage.

        Args:
            file_content: The file content as bytes
            file_path: The path where the file should be saved

        Returns:
            The path where the file was saved
        """
        raise NotImplementedError

    def get_file(self, file_path: str) -> bytes:
        """
        Retrieve file content from storage.

        Args:
            file_path: The path to the file

        Returns:
            The file content as bytes
        """
        raise NotImplementedError

    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from storage.

        Args:
            file_path: The path to the file to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        raise NotImplementedError

    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists in storage.

        Args:
            file_path: The path to check

        Returns:
            True if file exists, False otherwise
        """
        raise NotImplementedError


class LocalStorageBackend(StorageBackend):
    """Local filesystem storage backend"""

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_full_path(self, file_path: str) -> Path:
        """Get full path, ensuring it's within base_dir (prevent directory traversal)"""
        full_path = (self.base_dir / file_path).resolve()
        if not str(full_path).startswith(str(self.base_dir.resolve())):
            raise ValueError("Invalid file path: directory traversal detected")
        return full_path

    def save_file(self, file_content: bytes, file_path: str) -> str:
        """Save file to local filesystem"""
        full_path = self._get_full_path(file_path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(file_content)
        return str(full_path)

    def get_file(self, file_path: str) -> bytes:
        """Read file from local filesystem"""
        full_path = self._get_full_path(file_path)
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return full_path.read_bytes()

    def delete_file(self, file_path: str) -> bool:
        """Delete file from local filesystem"""
        try:
            full_path = self._get_full_path(file_path)
            if full_path.exists():
                full_path.unlink()
            return True
        except Exception:
            return False

    def file_exists(self, file_path: str) -> bool:
        """Check if file exists in local filesystem"""
        try:
            full_path = self._get_full_path(file_path)
            return full_path.exists()
        except Exception:
            return False


# Initialize default storage backend (local filesystem)
_storage_backend: Optional[StorageBackend] = None


def get_storage_backend() -> StorageBackend:
    """Get the current storage backend instance"""
    global _storage_backend
    if _storage_backend is None:
        _storage_backend = LocalStorageBackend(settings.UPLOAD_DIR)
    return _storage_backend


def set_storage_backend(backend: StorageBackend):
    """Set a custom storage backend (useful for testing or S3 migration)"""
    global _storage_backend
    _storage_backend = backend


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent directory traversal and other security issues.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename safe for storage
    """
    # Remove any path components
    filename = os.path.basename(filename)
    # Remove any null bytes
    filename = filename.replace("\x00", "")
    # Keep only alphanumeric, dots, hyphens, and underscores
    # This is conservative but safe
    safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_")
    filename = "".join(c if c in safe_chars else "_" for c in filename)
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext
    return filename or "unnamed_file"


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique, safe filename for storage.

    Args:
        original_filename: The original filename from the user

    Returns:
        A unique filename safe for storage
    """
    # Get file extension
    _, ext = os.path.splitext(original_filename)
    ext = ext.lower()

    # Generate unique ID
    unique_id = str(uuid.uuid4())

    # Create safe filename
    safe_name = sanitize_filename(original_filename)
    base_name, _ = os.path.splitext(safe_name)

    # Combine: unique_id_base_name.ext
    return f"{unique_id}_{base_name}{ext}"


def validate_file_size(file_size: int) -> None:
    """
    Validate that file size is within allowed limits.

    Args:
        file_size: File size in bytes

    Raises:
        HTTPException if file size exceeds limit
    """
    if file_size > settings.MAX_UPLOAD_SIZE:
        max_size_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {max_size_mb}MB",
        )


def validate_mime_type(mime_type: str) -> None:
    """
    Validate that MIME type is allowed (if whitelist is configured).

    Args:
        mime_type: The MIME type to validate

    Raises:
        HTTPException if MIME type is not allowed
    """
    if settings.ALLOWED_MIME_TYPES and mime_type not in settings.ALLOWED_MIME_TYPES:
        allowed_types = ", ".join(settings.ALLOWED_MIME_TYPES)
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{mime_type}' is not allowed. Allowed types: {allowed_types}",
        )


async def save_uploaded_file(
    upload_file: UploadFile, task_id: int, user_id: int
) -> tuple[str, str, int, str]:
    """
    Save an uploaded file and return metadata.

    Args:
        upload_file: FastAPI UploadFile object
        task_id: ID of the task this file belongs to
        user_id: ID of the user uploading the file

    Returns:
        Tuple of (filename, file_path, file_size, mime_type)

    Raises:
        HTTPException if validation fails
    """
    # Read file content
    content = await upload_file.read()
    file_size = len(content)

    # Validate file size
    validate_file_size(file_size)

    # Get MIME type
    mime_type = upload_file.content_type or "application/octet-stream"

    # Validate MIME type if whitelist is configured
    validate_mime_type(mime_type)

    # Generate safe, unique filename
    original_filename = upload_file.filename or "unnamed_file"
    filename = generate_unique_filename(original_filename)

    # Create storage path: task_{task_id}/user_{user_id}/{filename}
    file_path = f"task_{task_id}/user_{user_id}/{filename}"

    # Save file using storage backend
    storage = get_storage_backend()
    storage.save_file(content, file_path)

    return filename, file_path, file_size, mime_type


def get_file_content(file_path: str) -> bytes:
    """
    Retrieve file content from storage.

    Args:
        file_path: The storage path of the file

    Returns:
        File content as bytes

    Raises:
        FileNotFoundError if file doesn't exist
    """
    storage = get_storage_backend()
    return storage.get_file(file_path)


def delete_file(file_path: str) -> bool:
    """
    Delete a file from storage.

    Args:
        file_path: The storage path of the file to delete

    Returns:
        True if deletion was successful, False otherwise
    """
    storage = get_storage_backend()
    return storage.delete_file(file_path)
