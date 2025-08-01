# SPDX-FileCopyrightText: 2025 Knitli Inc.
# SPDX-FileContributor: Adam Poulemanos <adam@knit.li>
#
# SPDX-License-Identifier: MIT OR Apache-2.0

"""
Git repository data source implementation for CodeWeaver.

Provides content discovery from git repositories with branch/commit support,
version history tracking, and incremental synchronization capabilities.
"""

import logging

from collections.abc import Callable
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field

from codeweaver.cw_types import ContentItem, SourceCapabilities, SourceCapability
from codeweaver.sources.base import AbstractDataSource, SourceWatcher
from codeweaver.utils.decorators import not_implemented


logger = logging.getLogger(__name__)


class GitRepositorySourceConfig(BaseModel):
    """Configuration specific to git repository data sources."""

    model_config = ConfigDict(extra="allow", validate_assignment=True)
    enabled: Annotated[bool, Field(True, description="Whether source is enabled")]
    priority: Annotated[int, Field(1, ge=1, le=100, description="Source priority")]
    source_id: Annotated[str | None, Field(None, description="Unique source identifier")]
    include_patterns: Annotated[
        list[str], Field(default_factory=list, description="File patterns to include")
    ]
    exclude_patterns: Annotated[
        list[str], Field(default_factory=list, description="File patterns to exclude")
    ]
    max_file_size_mb: Annotated[int, Field(1, ge=1, le=1000, description="Maximum file size in MB")]
    batch_size: Annotated[int, Field(8, ge=1, le=1000, description="Batch size for processing")]
    max_concurrent_requests: Annotated[
        int, Field(10, ge=1, le=100, description="Maximum concurrent requests")
    ]
    request_timeout_seconds: Annotated[
        int, Field(30, ge=1, le=300, description="Request timeout in seconds")
    ]
    enable_change_watching: Annotated[bool, Field(False, description="Enable change watching")]
    change_check_interval_seconds: Annotated[
        int, Field(60, ge=1, le=3600, description="Change check interval in seconds")
    ]
    enable_content_deduplication: Annotated[
        bool, Field(True, description="Enable content deduplication")
    ]
    enable_metadata_extraction: Annotated[
        bool, Field(False, description="Enable metadata extraction")
    ]
    supported_languages: Annotated[
        list[str], Field(default_factory=list, description="Supported programming languages")
    ]
    repository_url: Annotated[str, Field(description="Git repository URL (required)")]
    local_clone_path: Annotated[
        str | None, Field(None, description="Local clone path for repository")
    ]
    branch: Annotated[str, Field("main", min_length=1, description="Git branch to checkout")]
    commit_hash: Annotated[str | None, Field(None, description="Specific commit hash to checkout")]
    depth: Annotated[int | None, Field(None, ge=1, description="Clone depth for shallow clones")]
    username: Annotated[str | None, Field(None, description="Username for authentication")]
    password: Annotated[str | None, Field(None, description="Password for authentication")]
    ssh_key_path: Annotated[str | None, Field(None, description="Path to SSH private key")]
    auto_pull: Annotated[bool, Field(True, description="Automatically pull updates")]
    pull_interval_minutes: Annotated[
        int, Field(30, ge=1, le=10080, description="Pull interval in minutes")
    ]
    track_file_history: Annotated[bool, Field(False, description="Track file history and changes")]
    include_commit_metadata: Annotated[
        bool, Field(True, description="Include commit metadata in content items")
    ]


@not_implemented
class GitRepositorySourceProvider(AbstractDataSource):
    """Git repository data source implementation.

    Provides content discovery from git repositories with support for
    different branches, commits, and incremental synchronization.

    Note: This is a placeholder implementation. Full git integration
    would require additional dependencies like GitPython or pygit2.
    """

    def __init__(self, source_id: str | None = None):
        """Initialize git repository data source.

        Args:
            source_id: Unique identifier for this source instance
        """
        super().__init__("git", source_id)

    @classmethod
    def check_availability(cls, capability: SourceCapability) -> tuple[bool, str | None]:
        """Check if git repository source is available for the given capability."""
        supported_capabilities = {
            SourceCapability.CONTENT_DISCOVERY,
            SourceCapability.CONTENT_READING,
            SourceCapability.CHANGE_WATCHING,
            SourceCapability.INCREMENTAL_SYNC,
            SourceCapability.VERSION_HISTORY,
            SourceCapability.METADATA_EXTRACTION,
            SourceCapability.BATCH_PROCESSING,
            SourceCapability.AUTHENTICATION,
        }
        if capability in supported_capabilities:
            import shutil

            if shutil.which("git") is None:
                return (False, "git command not found in PATH")
            return (True, None)
        return (False, f"Capability {capability.value} not supported by Git source")

    def get_capabilities(self) -> SourceCapabilities:
        """Get capabilities supported by git repository source."""
        return SourceCapabilities(
            supports_content_discovery=True,
            supports_content_reading=True,
            supports_change_watching=True,
            supports_incremental_sync=True,
            supports_version_history=True,
            supports_metadata_extraction=True,
            supports_batch_processing=True,
            supports_authentication=True,
        )

    async def discover_content(self, config: GitRepositorySourceConfig) -> list[ContentItem]:
        """Discover files from a git repository.

        Args:
            config: Git repository source configuration

        Returns:
            List of discovered content items

        Raises:
            NotImplementedError: This is a placeholder implementation
        """
        if not config.get("enabled", True):
            return []
        if repository_url := config.get("repository_url"):
            raise NotImplementedError(
                "Git repository source is not yet implemented. Future implementation will require GitPython or pygit2 dependency."
            )
        raise ValueError("repository_url is required for git source")

    async def read_content(self, item: ContentItem) -> str:
        """Read content from a git repository file.

        Args:
            item: Content item representing a git file

        Returns:
            Text content of the file

        Raises:
            NotImplementedError: This is a placeholder implementation
        """
        if item.content_type != "git":
            raise ValueError(f"Unsupported content type for git source: {item.content_type}")
        raise NotImplementedError("Git content reading not yet implemented")

    async def watch_changes(
        self, config: GitRepositorySourceConfig, callback: Callable[[list[ContentItem]], None]
    ) -> SourceWatcher:
        """Set up git repository change watching.

        Args:
            config: Git repository source configuration
            callback: Function to call when changes are detected

        Returns:
            Watcher for git repository changes

        Raises:
            NotImplementedError: This is a placeholder implementation
        """
        if not config.get("enable_change_watching", False):
            raise NotImplementedError("Change watching is disabled in configuration")
        raise NotImplementedError("Git change watching not yet implemented")

    async def validate_source(self, config: GitRepositorySourceConfig) -> bool:
        """Validate git repository source configuration.

        Args:
            config: Configuration to validate

        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            if not await super().validate_source(config):
                return False
            repository_url = config.get("repository_url")
            if not repository_url:
                logger.warning("Missing repository_url in git source configuration")
                return False
            logger.warning("Git repository validation not fully implemented")
        except Exception:
            logger.exception("Error validating git repository source configuration")
            return False
        else:
            return True

    async def get_content_metadata(self, item: ContentItem) -> dict[str, Any]:
        """Get detailed metadata for a git repository file.

        Args:
            item: Content item representing a git file

        Returns:
            Dictionary with detailed git metadata
        """
        metadata = await super().get_content_metadata(item)
        metadata.update({
            "git_metadata_available": False,
            "implementation_note": "Git metadata extraction not yet implemented",
        })
        return metadata

    async def health_check(self) -> bool:
        """Check git data source health by verifying repository accessibility.

        Returns:
            True if source is healthy and operational, False otherwise
        """
        try:
            if not hasattr(self, "source_id") or not self.source_id:
                logger.warning("Git source missing source_id")
                return False
            test_path = Path(".")
            git_dir = test_path / ".git"
            if git_dir.exists():
                logger.debug("Git source health check passed - found .git directory")
                return True
            current = test_path
            for _ in range(5):
                current = current.parent
                if (current / ".git").exists():
                    logger.debug("Git source health check passed - found .git in parent")
                    return True
            logger.warning("Git source health check failed - no .git directory found")
        except Exception:
            logger.exception("Git source health check failed")
            return False
        else:
            return False
