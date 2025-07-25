# SPDX-FileCopyrightText: 2025 Knitli Inc.
# SPDX-FileContributor: Adam Poulemanos <adam@knit.li>
#
# SPDX-License-Identifier: MIT OR Apache-2.0

"""Service configuration types for CodeWeaver."""

from pathlib import Path
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field

from codeweaver._types.enums import ChunkingStrategy, PerformanceMode


class ServiceConfig(BaseModel):
    """Base configuration for all services."""

    model_config = ConfigDict(extra="allow", validate_assignment=True)

    enabled: Annotated[bool, Field(description="Whether service is enabled")] = True
    provider: Annotated[str, Field(description="Service provider name")]
    priority: Annotated[int, Field(ge=0, le=100, description="Service priority")] = 50
    timeout: Annotated[float, Field(gt=0, description="Timeout in seconds")] = 30.0
    max_retries: Annotated[int, Field(ge=0, description="Max retry attempts")] = 3
    retry_delay: Annotated[float, Field(ge=0, description="Retry delay in seconds")] = 1.0
    health_check_interval: Annotated[float, Field(gt=0, description="Health check interval")] = 60.0
    tags: Annotated[list[str], Field(description="Service tags")] = Field(default_factory=list)
    metadata: Annotated[dict[str, Any], Field(description="Additional metadata")] = Field(
        default_factory=dict
    )


class ChunkingServiceConfig(ServiceConfig):
    """Configuration for chunking services."""

    provider: str = "fastmcp_chunking"
    max_chunk_size: Annotated[int, Field(gt=0, le=10000, description="Max chunk size")] = 1500
    min_chunk_size: Annotated[int, Field(gt=0, le=1000, description="Min chunk size")] = 50
    overlap_size: Annotated[int, Field(ge=0, description="Chunk overlap size")] = 100
    ast_grep_enabled: Annotated[bool, Field(description="Enable AST chunking")] = True
    fallback_strategy: Annotated[ChunkingStrategy, Field(description="Fallback strategy")] = (
        ChunkingStrategy.SIMPLE
    )
    performance_mode: Annotated[PerformanceMode, Field(description="Performance mode")] = (
        PerformanceMode.BALANCED
    )

    # Language-specific configurations
    language_configs: Annotated[
        dict[str, dict[str, Any]], Field(description="Language-specific configs")
    ] = Field(default_factory=dict)

    # Advanced chunking options
    respect_code_structure: Annotated[
        bool, Field(description="Respect code structure boundaries")
    ] = True
    preserve_comments: Annotated[bool, Field(description="Keep comments with code")] = True
    include_imports: Annotated[bool, Field(description="Include import statements")] = True


class FilteringServiceConfig(ServiceConfig):
    """Configuration for filtering services."""

    provider: str = "fastmcp_filtering"
    include_patterns: Annotated[list[str], Field(description="Include patterns")] = Field(
        default_factory=list
    )
    exclude_patterns: Annotated[list[str], Field(description="Exclude patterns")] = Field(
        default_factory=list
    )
    max_file_size: Annotated[int, Field(gt=0, description="Max file size in bytes")] = 1024 * 1024
    max_depth: Annotated[int | None, Field(ge=0, description="Max directory depth")] = None
    follow_symlinks: Annotated[bool, Field(description="Follow symlinks")] = False
    ignore_hidden: Annotated[bool, Field(description="Ignore hidden files")] = True
    use_gitignore: Annotated[bool, Field(description="Respect .gitignore")] = True
    parallel_scanning: Annotated[bool, Field(description="Enable parallel scanning")] = True
    max_concurrent_scans: Annotated[int, Field(gt=0, description="Max concurrent scans")] = 10

    # File type filtering
    allowed_extensions: Annotated[list[str], Field(description="Allowed file extensions")] = Field(
        default_factory=list
    )
    blocked_extensions: Annotated[list[str], Field(description="Blocked file extensions")] = Field(
        default_factory=list
    )

    # Directory filtering
    ignore_directories: Annotated[list[str], Field(description="Directories to ignore")] = Field(
        default_factory=lambda: [
            ".git",
            ".svn",
            ".hg",
            ".bzr",
            "node_modules",
            "__pycache__",
            ".pytest_cache",
            "build",
            "dist",
            "target",
            ".next",
            ".nuxt",
            ".venv",
            "venv",
            ".env",
        ]
    )


class ValidationServiceConfig(ServiceConfig):
    """Configuration for validation services."""

    provider: str = "default_validation"
    validation_level: Annotated[str, Field(description="Validation strictness level")] = "standard"
    max_errors_per_item: Annotated[
        int, Field(ge=0, description="Max errors per validation item")
    ] = 10
    stop_on_first_error: Annotated[bool, Field(description="Stop validation on first error")] = (
        False
    )
    parallel_validation: Annotated[bool, Field(description="Enable parallel validation")] = True
    max_concurrent_validations: Annotated[
        int, Field(gt=0, description="Max concurrent validations")
    ] = 5
    cache_results: Annotated[bool, Field(description="Cache validation results")] = True
    result_cache_ttl: Annotated[int, Field(gt=0, description="Result cache TTL in seconds")] = 3600

    # Rule configuration
    enable_syntax_validation: Annotated[bool, Field(description="Enable syntax validation")] = True
    enable_style_validation: Annotated[bool, Field(description="Enable style validation")] = False
    enable_security_validation: Annotated[bool, Field(description="Enable security validation")] = (
        True
    )
    enable_performance_validation: Annotated[
        bool, Field(description="Enable performance validation")
    ] = False

    # Custom rules
    custom_rules: Annotated[list[dict[str, Any]], Field(description="Custom validation rules")] = (
        Field(default_factory=list)
    )


class CacheServiceConfig(ServiceConfig):
    """Configuration for cache services."""

    provider: str = "memory_cache"
    max_size: Annotated[int, Field(gt=0, description="Maximum cache size in bytes")] = (
        100 * 1024 * 1024
    )  # 100MB
    max_items: Annotated[int, Field(gt=0, description="Maximum number of cached items")] = 10000
    default_ttl: Annotated[int, Field(gt=0, description="Default TTL in seconds")] = 3600
    eviction_policy: Annotated[str, Field(description="Cache eviction policy")] = "lru"
    persistence_enabled: Annotated[bool, Field(description="Enable cache persistence")] = False
    persistence_path: Annotated[Path | None, Field(description="Path for cache persistence")] = None
    compression_enabled: Annotated[bool, Field(description="Enable cache compression")] = False
    metrics_enabled: Annotated[bool, Field(description="Enable cache metrics")] = True

    # Cache partitioning
    enable_partitioning: Annotated[bool, Field(description="Enable cache partitioning")] = False
    partition_count: Annotated[int, Field(gt=0, description="Number of cache partitions")] = 4

    # Advanced options
    cleanup_interval: Annotated[int, Field(gt=0, description="Cleanup interval in seconds")] = 300
    stats_collection_interval: Annotated[
        int, Field(gt=0, description="Stats collection interval")
    ] = 60


class MonitoringServiceConfig(ServiceConfig):
    """Configuration for monitoring services."""

    provider: str = "default_monitoring"
    check_interval: Annotated[
        float, Field(gt=0, description="Health check interval in seconds")
    ] = 30.0
    alert_threshold: Annotated[
        float, Field(ge=0, le=1, description="Alert threshold for health")
    ] = 0.8
    enable_alerts: Annotated[bool, Field(description="Enable alerting")] = True
    enable_auto_recovery: Annotated[bool, Field(description="Enable automatic recovery")] = True
    max_recovery_attempts: Annotated[int, Field(ge=0, description="Maximum recovery attempts")] = 3
    recovery_delay: Annotated[float, Field(ge=0, description="Delay between recovery attempts")] = (
        10.0
    )

    # Monitoring targets
    monitor_performance: Annotated[bool, Field(description="Monitor performance metrics")] = True
    monitor_memory: Annotated[bool, Field(description="Monitor memory usage")] = True
    monitor_disk: Annotated[bool, Field(description="Monitor disk usage")] = False
    monitor_network: Annotated[bool, Field(description="Monitor network metrics")] = False


class MetricsServiceConfig(ServiceConfig):
    """Configuration for metrics services."""

    provider: str = "default_metrics"
    collection_interval: Annotated[
        float, Field(gt=0, description="Metrics collection interval")
    ] = 60.0
    retention_period: Annotated[
        int, Field(gt=0, description="Metrics retention period in seconds")
    ] = 86400  # 24 hours
    enable_aggregation: Annotated[bool, Field(description="Enable metrics aggregation")] = True
    aggregation_window: Annotated[int, Field(gt=0, description="Aggregation window in seconds")] = (
        300  # 5 minutes
    )

    # Export options
    enable_export: Annotated[bool, Field(description="Enable metrics export")] = False
    export_format: Annotated[str, Field(description="Export format")] = "json"
    export_path: Annotated[Path | None, Field(description="Export file path")] = None
    export_interval: Annotated[int, Field(gt=0, description="Export interval in seconds")] = 300

    # Metric types to collect
    collect_performance_metrics: Annotated[
        bool, Field(description="Collect performance metrics")
    ] = True
    collect_resource_metrics: Annotated[bool, Field(description="Collect resource metrics")] = True
    collect_business_metrics: Annotated[bool, Field(description="Collect business metrics")] = False


class ServicesConfig(BaseModel):
    """Root configuration for all services."""

    chunking: Annotated[ChunkingServiceConfig, Field(description="Chunking config")] = Field(
        default_factory=ChunkingServiceConfig
    )
    filtering: Annotated[FilteringServiceConfig, Field(description="Filtering config")] = Field(
        default_factory=FilteringServiceConfig
    )
    validation: Annotated[ValidationServiceConfig, Field(description="Validation config")] = Field(
        default_factory=ValidationServiceConfig
    )
    cache: Annotated[CacheServiceConfig, Field(description="Cache config")] = Field(
        default_factory=CacheServiceConfig
    )
    monitoring: Annotated[MonitoringServiceConfig, Field(description="Monitoring config")] = Field(
        default_factory=MonitoringServiceConfig
    )
    metrics: Annotated[MetricsServiceConfig, Field(description="Metrics config")] = Field(
        default_factory=MetricsServiceConfig
    )

    # Global service settings
    global_timeout: Annotated[float, Field(gt=0, description="Global timeout")] = 300.0
    health_check_enabled: Annotated[bool, Field(description="Enable health checks")] = True
    metrics_enabled: Annotated[bool, Field(description="Enable metrics")] = True
    auto_recovery: Annotated[bool, Field(description="Enable auto recovery")] = True

    # Service discovery and registration
    enable_service_discovery: Annotated[bool, Field(description="Enable service discovery")] = False
    service_discovery_interval: Annotated[float, Field(gt=0, description="Discovery interval")] = (
        60.0
    )

    # Performance settings
    max_concurrent_services: Annotated[int, Field(gt=0, description="Max concurrent services")] = 10
    service_startup_timeout: Annotated[
        float, Field(gt=0, description="Service startup timeout")
    ] = 30.0
    service_shutdown_timeout: Annotated[
        float, Field(gt=0, description="Service shutdown timeout")
    ] = 10.0
