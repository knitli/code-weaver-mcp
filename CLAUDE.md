<!--
SPDX-FileCopyrightText: 2025 Knitli Inc.
SPDX-FileContributor: Adam Poulemanos <adam@knit.li>

SPDX-License-Identifier: MIT OR Apache-2.0
-->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CodeWeaver is an extensible Model Context Protocol (MCP) server built on factory patterns and protocol-based interfaces. It provides semantic code search through a plugin architecture supporting multiple embedding providers, vector databases, and data sources.

**Key Architecture Features:**
- **Extensible Plugin System**: Factory pattern with runtime component discovery
- **Protocol-Based Interfaces**: Universal abstractions for providers, backends, sources, and services
- **Service Layer Architecture**: Clean abstraction layer connecting middleware with factory patterns
- **Configuration-Driven**: Hierarchical config system with environment variables and TOML files
- **Multiple Provider Support**: Voyage AI, OpenAI, Cohere, HuggingFace, and custom providers
- **Multiple Backend Support**: Qdrant, Pinecone, Weaviate, ChromaDB, and custom backends
- **Universal Data Sources**: Filesystem, Git, Database, API, Web, and custom sources
- **ast-grep Integration**: Tree-sitter based structural search for 20+ programming languages
- **FastMCP Middleware**: Cross-cutting concerns and request processing with service injection

## Architecture

### Core Components

- **`src/codeweaver/main.py`**: Server entry point with configuration-driven initialization
- **`src/codeweaver/server.py`**: Clean server implementation using plugin system and FastMCP middleware
- **`src/codeweaver/__init__.py`**: Package-level documentation and version info
- **`src/codeweaver/assistant_guide.md`**: Comprehensive usage guide for AI assistants

### Extended CodeWeaver Architecture

The project implements a comprehensive extensible architecture with the factory pattern as its foundation:

- **`src/codeweaver/`**: Core extensible server implementation
  - **`server.py`**: Clean server using plugin system and FastMCP middleware
  - **`config.py`**: Hierarchical configuration management system
  - **`_types/`**: Centralized type system with protocols, enums, and data structures
  - **`factories/`**: Factory pattern implementations for extensibility and plugin discovery
    - **`codeweaver_factory.py`**: Main orchestrator for unified component creation including services
    - **`backend_registry.py`**: Vector database backend registration and management
    - **`source_registry.py`**: Data source registration and management
    - **`service_registry.py`**: Service provider registration and lifecycle management
    - **`plugin_protocols.py`**: Plugin interface definitions and validation
    - **`extensibility_manager.py`**: Overall plugin system coordination
  - **`providers/`**: Embedding and reranking provider abstraction (Voyage AI, OpenAI, Cohere, HuggingFace, Custom)
  - **`backends/`**: Vector database abstraction (Qdrant, Pinecone, Weaviate, ChromaDB, Custom)
  - **`sources/`**: Universal data source abstraction (Filesystem, Git, Database, API, Web, Custom)
  - **`services/`**: Service layer architecture connecting middleware with factory patterns
    - **`manager.py`**: ServicesManager for coordinating all services with health monitoring
    - **`middleware_bridge.py`**: Bridge between FastMCP middleware and service layer
    - **`providers/`**: Service provider implementations (chunking, filtering, validation, etc.)
  - **`middleware/`**: FastMCP middleware for chunking, filtering, and cross-cutting concerns
  - **`client/`**: Client utilities and logging infrastructure
  - **`testing/`**: Testing utilities and framework helpers (NOT actual tests)

### Test Organization

Tests are organized by type and purpose:

- **`tests/unit/`**: Unit tests for individual components
  - `test_factory_system.py`: Factory pattern tests
  - `test_factory_validation.py`: Factory validation tests
  - `test_protocol_compliance.py`: Protocol compliance tests

- **`tests/integration/`**: Integration tests for system components
  - `test_integration.py`: General integration tests
  - `test_benchmarks.py`: Performance benchmarks
  - `test_server_functionality.py`: Server functionality tests
  - `test_service_integration.py`: Service layer integration tests

- **`tests/validation/`**: Validation scripts for architecture and implementation
  - `validate_service_implementation.py`: Service layer compliance validation

### Key Classes and Architecture Components

#### Factory System
1. **`CodeWeaverFactory`**: Main orchestrator for unified component creation and dependency injection
2. **`BackendRegistry`**: Manages vector database backend registration, validation, and creation
3. **`SourceRegistry`**: Manages data source registration, validation, and creation
4. **`ServiceRegistry`**: Manages service provider registration, validation, and creation
5. **`ExtensibilityManager`**: Coordinates plugin discovery, validation, and lifecycle management
6. **`PluginDiscoveryEngine`**: Handles entry point scanning, directory scanning, and module introspection

#### Core Server Components
7. **`CodeWeaverServer`**: Main MCP server using plugin system and FastMCP middleware
8. **`ConfigManager`**: Hierarchical configuration system with TOML and environment variable support
9. **`ServicesManager`**: Coordinates all services with health monitoring and auto-recovery

#### Protocol-Based Interfaces
10. **`VectorBackend`**: Universal protocol for vector database operations
11. **`EmbeddingProvider`**: Universal protocol for embedding and reranking operations
12. **`DataSource`**: Universal protocol for content discovery and processing
13. **`ServiceProvider`**: Universal protocol for service lifecycle and health management
14. **`ChunkingService`**: Protocol for content chunking services
15. **`FilteringService`**: Protocol for file filtering and discovery services
16. **`PluginInterface`**: Universal protocol for plugin registration and validation

#### Data Structures
17. **`ContentItem`**: Universal content representation across all data sources
18. **`ComponentInfo`**: Metadata for component registration and capabilities
19. **`PluginInfo`**: Plugin metadata and validation information
20. **`ServiceHealth`**: Health status and metrics for service monitoring
21. **`ServicesConfig`**: Hierarchical configuration for all services

## Common Development Commands

### Environment Setup
```bash
# Install dependencies using uv (fast Python package manager)
uv sync

# Install development dependencies
uv sync --group dev

# Create virtual environment (if needed)
uv venv

# Activate virtual environment
source .venv/bin/activate
```

### Running the Server
```bash
# Run the MCP server directly
uv run python src/codeweaver/main.py

# Run using the CLI entry point
uv run codeweaver

# Run with environment variables
CW_EMBEDDING_API_KEY=your_key CW_VECTOR_BACKEND_URL=your_url uv run codeweaver
```

### Code Quality & Linting
```bash
# Run linting with ruff
uv run ruff check

# Auto-fix linting issues
uv run ruff check --fix

# Format code
uv run ruff format

# Check specific files
uv run ruff check src/codeweaver/main.py
```

### Testing

Full [testing guide here](tests/README.md).
The project has a comprehensive test suite organized by type:

```bash
# Run all tests
uv run pytest

# Run unit tests only
uv run pytest tests/unit/

# Run integration tests
uv run pytest tests/integration/

# Run validation scripts
uv run python tests/validation/validate_architecture.py
uv run python tests/validation/test_provider_system.py

# Run specific test file
uv run pytest tests/unit/test_factory_system.py

# Run with coverage
uv run pytest --cov=codeweaver tests/

# Run benchmarks
uv run python tests/integration/test_benchmarks.py

# Test server functionality manually
uv run python tests/integration/test_server_functionality.py /path/to/test/codebase

# Test service layer integration
uv run python tests/integration/test_service_integration.py

# Validate service implementation
uv run python tests/validation/validate_service_implementation.py
```

### Building and Distribution
```bash
# Build the package
uv build

# Publish to PyPI (requires credentials)
uv publish
```

## Configuration Files

- **`pyproject.toml`**: Project metadata, dependencies, and build configuration
- **`ruff.toml`**: Comprehensive linting and formatting rules
- **`mise.toml`**: Development environment tool management
- **`.mcp.json`**: MCP server configuration for Claude Desktop
- **`uv.lock`**: Dependency lockfile for reproducible builds

## MCP Tools Provided

The server exposes four main tools:

1. **`index_codebase`**: Semantically chunk and embed a codebase for search
2. **`search_code`**: Natural language search with advanced filtering options
3. **`ast_grep_search`**: Structural search using ast-grep patterns
4. **`get_supported_languages`**: List supported languages and capabilities

## Environment Variables Required

- **`CW_EMBEDDING_API_KEY`**: Your embedding provider API key (required)
- **`CW_VECTOR_BACKEND_URL`**: Your vector database URL (required)
- **`CW_VECTOR_BACKEND_API_KEY`**: Your vector database API key (optional if no auth)
- **`CW_VECTOR_BACKEND_COLLECTION`**: Vector collection name (defaults to "codeweaver-UUID4")

## Service Layer Architecture

CodeWeaver implements a comprehensive service layer that provides clean abstraction between FastMCP middleware and the factory pattern system. This architecture enables dependency injection, health monitoring, and extensible service providers.

### Service Types

**Core Services** (required for basic operation):
- **Chunking Service**: Intelligent code segmentation using ast-grep with fallback parsing
- **Filtering Service**: File discovery and filtering with gitignore support

**Optional Services** (enhanced functionality):
- **Validation Service**: Content validation with configurable rules
- **Cache Service**: Performance optimization through intelligent caching
- **Monitoring Service**: Health monitoring and auto-recovery
- **Metrics Service**: Performance metrics collection and analysis

### Service Provider Architecture

```python
# Example: Creating and using services
from codeweaver.cw_types import ServiceType, ServicesConfig
from codeweaver.services.manager import ServicesManager

# Initialize services
config = ServicesConfig()
services_manager = ServicesManager(config)
await services_manager.initialize()

# Get services through dependency injection
chunking_service = services_manager.get_chunking_service()
filtering_service = services_manager.get_filtering_service()

# Use services
chunks = await chunking_service.chunk_content(content, file_path)
files = await filtering_service.discover_files(base_path)
```

### Middleware Integration

The service layer integrates seamlessly with FastMCP middleware through the ServiceBridge:

```python
from codeweaver.services.middleware_bridge import ServiceBridge
from codeweaver.services.manager import ServicesManager

# Create service bridge
services_manager = ServicesManager(config)
service_bridge = ServiceBridge(services_manager)

# Services are automatically injected into tool contexts
# Tools can access services via context.fastmcp_context.get_state_value("chunking_service")
```

### Service Configuration

Services are configured through a hierarchical configuration system:

```python
from codeweaver.cw_types import ServicesConfig, ChunkingServiceConfig

# Configure services
services_config = ServicesConfig(
    chunking=ChunkingServiceConfig(
        provider="fastmcp_chunking",
        max_chunk_size=1500,
        min_chunk_size=50,
        ast_grep_enabled=True,
        performance_mode="balanced"
    ),
    filtering=FilteringServiceConfig(
        provider="fastmcp_filtering",
        use_gitignore=True,
        max_file_size=1024*1024,
        parallel_scanning=True
    )
)
```

### Health Monitoring

All services implement comprehensive health monitoring:

```python
# Get health report for all services
health_report = await services_manager.get_health_report()
print(f"Overall status: {health_report.overall_status}")

# Check individual service health
chunking_health = await chunking_service.health_check()
print(f"Chunking service: {chunking_health.status}")
```

### Creating Custom Services

Implement custom services by extending the base provider and implementing the service protocol:

```python
from codeweaver.services.providers.base_provider import BaseServiceProvider
from codeweaver.cw_types import ValidationService

class CustomValidationProvider(BaseServiceProvider, ValidationService):
    async def _initialize_provider(self) -> None:
        # Initialize your service
        pass

    async def validate_content(self, content, rules=None):
        # Implement validation logic
        pass

# Register with factory
factory.register_service_provider(
    ServiceType.VALIDATION,
    "custom_validation",
    CustomValidationProvider
)
```

### Service Plugin Development

Services can be extended through plugins:

```python
# Plugin interface for services
class ServicePlugin:
    def get_service_class(self):
        return MyCustomServiceProvider

    @property
    def service_type(self):
        return ServiceType.VALIDATION
```

## Language Support

The system supports 20+ programming languages with proper AST-aware chunking:

**Web**: HTML, CSS, JavaScript, TypeScript, React TSX, Vue, Svelte
**Systems**: Rust, Go, C/C++, C#, Zig
**High-level**: Python, Java, Kotlin, Scala, Ruby, PHP, Swift, Dart
**Functional**: Haskell, OCaml, Elm, Elixir, Erlang, Clojure
**Data**: JSON, YAML, TOML, XML, SQL
**Scripts**: Bash, PowerShell, Docker, Make, CMake

## Development Notes

### Repository Practices

See guides:
- docs/DEVELOPMENT_PATTERNS.md
- docs/SERVICES_LAYER_GUIDE.md

### Code Style
- Uses Google docstring convention with plain language, active voice, and present tense
- Line length: 100 characters
- Auto-fixes enabled in ruff configuration
- Type hints required for public functions (encouraged for all)
- Use modern Python typing (>=3.11): `typing.Self`, `typing.Literal`, piped unions (`int | str`), constructors-as-types (`list[str]`), etc.
- **strong typing**: Use `typing.TypedDict` for structured data, `typing.Protocol` for interfaces, `typing.NamedTuple` for immutable data structures, `enum.Enum` types for fixed sets of values, `typing.TypeGuard` for type validation.
  - Avoid generic types like dict[str, Any] if your know the structure -- use TypedDict or NamedTuple instead.
  - If something is actually generic, define a generic type, or a protocol, or a type guard.
- **Use pydantic (v2)** for serialization/deserialization and validation of complex data structures
  - Use `pydantic.BaseModel` for models, `pydantic.Field` for field definitions in the format:
    ```python
    from typing import Annotated

    from pydantic import BaseModel, Field

    class MyModel(BaseModel):
        name: Annotated[str, Field(description="The name of the item")]
        value: Annotated[int, Field(ge=0, description="The value must be non-negative")] = 0
    ```
  - Use `pydantic.ConfigDict` for model configuration (e.g., `extra = "forbid"` to disallow extra fields, but usually you want `extra = "allow"` to allow extra fields for anything plugin-like)

### Avoid these Linting Issues (they're common and take FOREVER to fix)
- Logging:
  - **NEVER** use f-strings in logging calls (e.g., `logger.info(f"Value: {value}")`), use `logger.info("Value: %s", value)` instead.
  - **No print statements** in production code, use logging instead.
  - **Use logging.exception** for exceptions, not `logger.error` or `logger.warning`
    - **DO NOT ADD THE EXCEPTION** to the log message, it will be added automatically.

- Try blocks:
  - **Avoid bare excepts**: Always specify the exception type (e.g., `except ValueError:`)
  - **Avoid returns at end of `try` blocks**: Use `else` for return statements after `try` to ensure clarity (early returns in the block are fine).
  - **Don't raise exceptions inside `try` blocks**: Use an inside function outside the `try` block to raise exceptions.

- Except blocks:
  - **Use raise from** when re-raising exceptions to maintain context (e.g., `raise MyException("message") from original_exception`)
  - **Do not use except blocks to suppress exceptions** Use `contextlib.suppress` for specific cases where you want to ignore exceptions.

- Function Definitions:
  - all arguments and return values must have type annotations (including `myfun() -> None`).
  - **No Boolean-typed *positional* arguments**: Use keyword arguments for booleans by separating them with `*`, as in:

    ```python
    def my_function(arg1: str, *, flag: bool = False) -> None:
        pass
    ```
- Generally follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for code style and conventions.

### Dependencies
- **Production**: `ast-grep-py`, `fastmcp`, `qdrant-client`, `rignore`, `watchdog`
- **Development**: `pytest`, `ruff`, `uv`
- **Build**: Uses `uv_build` backend

### Design Principles

- **Simplicity**: Keep the codebase clean and maintainable
- **Configurability**: If there's a setting, it should be configurable via environment variables or config files
- **Extensibility**: Design for future features and integrations, plugin architecture
- **Performance**: Optimize for large codebases with efficient chunking and search
- **Robustness**: Handle errors gracefully, especially with external dependencies like ast-grep
- **Security**: Validate all inputs, especially from external sources

### Project Organization Principles

- **Clear Separation**: Tests, examples, and utilities are kept in separate directories
  - Tests live in `tests/` organized by type (unit, integration, validation)
  - Examples live in `examples/` including migration guides (though this is a new tool and has nothing to migrate from yet)
  - Test utilities live in `src/codeweaver/testing/` (not actual tests)
- **No Mixed Concerns**: Production code should not contain examples or test code
- **Idiomatic Structure**: Follow Python packaging best practices
  - Source code in `src/`
  - Tests in `tests/` at project root
  - Examples in `examples/` at project root
  - Documentation in project root and inline

### Type Organization Guidelines

The codebase follows a strict type organization system to maintain consistency and avoid circular dependencies:

#### **Types That BELONG in `src/codeweaver/_types/`** (Centralized, Reusable)

1. **Pure Data Types**: TypedDict, NamedTuple, dataclass, Pydantic models representing data structures
   - Examples: `ContentItem`, `PluginInfo`, `ComponentLifecycle`
2. **Enums**: All enum types representing standardized sets of values
   - Examples: `ComponentState`, `SearchComplexity`, `ErrorSeverity`
3. **Type Aliases**: NewType definitions, generic type aliases
   - Examples: `DimensionSize`, type variables like `T`
4. **Universal Protocols**: Protocols used across multiple modules
   - Examples: Base capability protocols, component interfaces
5. **Core Configuration Types**: Base configuration models used by multiple components
   - Examples: `BaseComponentConfig`, `ValidationLevel`
6. **Registry Data Structures**: Information models for component registration
   - Examples: Registry entries, component metadata
7. **Cross-Domain Exception Types**: Exception types that multiple modules need to catch or raise
   - Examples: `BackendError`, `CodeWeaverFactoryError`, `ComponentNotFoundError`

#### **Types That STAY in Their Module** (Module-Specific, Tightly Coupled)

1. **Business Logic Classes**: Concrete implementations of functionality
   - Examples: `QdrantBackend`, `VoyageEmbedder`, actual service classes
2. **Module-Specific Protocols**: Protocols only used within one module
   - Examples: Provider-specific interfaces, backend-specific protocols
3. **Implementation-Specific Config**: Configuration that extends base types for specific implementations
   - Examples: `VoyageConfig`, `QdrantConfig`, provider-specific settings
4. **Factory Classes**: Classes that create/manage other classes within the module
   - Examples: Module-specific factories, registries that manage local resources
5. **Module-Specific Exceptions**: Error types specific to one module's operation (that others don't need to catch)
   - Examples: Provider connection errors, backend-specific validation errors

#### **Import Guidelines**

- **For centralized types**: `from codeweaver.cw_types import TypeName, AnotherType`
- **For module-specific types**: Import from the specific module where they're defined
- **Avoid circular imports**: Types in `_types/` should not import from other modules except for essential dependencies

#### **Current `_types/` Module Structure**

```
src/codeweaver/_types/
├── __init__.py          # Single import point for all types
├── backends.py          # Backend data structures (VectorPoint, SearchResult, etc.)
├── base_enum.py         # Base enum class for consistent enum behavior
├── capabilities.py      # Capability query interfaces and models
├── config.py           # Core configuration types and enums
├── core.py             # Universal protocols and core interfaces
├── data_structures.py  # Cross-module data structures (PluginInfo, ContentItem, etc.)
├── enums.py            # Cross-module enums (ComponentState, SearchComplexity, etc.)
├── exceptions.py       # Cross-module exception types
├── provider_*.py       # Provider-related types and registries
├── source_*.py         # Source-related types and registries
├── service_*.py        # Service-related types and protocols
└── services.py         # Service protocol interfaces
```

This organization ensures clean separation of concerns, prevents circular dependencies, and makes the codebase more maintainable by centralizing reusable types while keeping implementation-specific types close to their usage.

### Key Design Decisions
- **Semantic chunking**: Uses ast-grep for intelligent code segmentation
- **Hybrid search**: Combines semantic embeddings with structural patterns
- **Fallback parsing**: Graceful degradation when ast-grep unavailable
- **Batched processing**: Efficient handling of large codebases
- **Smart filtering**: File type, language, and directory-based filtering
- **Service layer**: Clean abstraction connecting middleware with factory patterns
- **Protocol-based DI**: Runtime-checkable protocols for dependency injection
- **Health monitoring**: Comprehensive service health tracking with auto-recovery

### Performance Considerations
- Chunks limited to 1500 characters max, 50 characters min
- Files larger than 1MB are skipped during indexing
- Batch processing (8 files at a time) for memory efficiency
- Automatic ignoring of common build/cache directories

## Integration Examples

### Claude Desktop Configuration
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "codeweaver": {
      "command": "uv",
      "args": ["run", "codeweaver"],
      "env": {
        "CW_EMBEDDING_API_KEY": "your-key",
        "CW_VECTOR_BACKEND_URL": "your-url",
        "CW_VECTOR_BACKEND_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Typical Usage Flow
1. Index a codebase: `index_codebase` with project root path
2. Search semantically: `search_code` with natural language queries
3. Find patterns: `ast_grep_search` with structural patterns
4. Get language info: `get_supported_languages` for capabilities

## Troubleshooting

### Common Issues
- **"ast-grep not available"**: Install with `uv add ast-grep-py`
- **API key errors**: Verify Voyage AI credentials
- **No results**: Ensure codebase is indexed first
- **Large files skipped**: Files >1MB are automatically excluded

## Directory Structure Reference

When working with this codebase, navigate to these directories:

- **Source Code**: `src/codeweaver/` for production code, `src/codeweaver/` for MCP server
- **Tests**: `tests/unit/`, `tests/integration/`, `tests/validation/`
- **Examples**: `examples/` for usage examples, `examples/migration/` for migration guides
- **Test Utilities**: `src/codeweaver/testing/` (helper functions, not actual tests)

## Important Instruction Reminders
Do what has been asked; nothing more, nothing less.
- Only create files if they're absolutely necessary for achieving your goal. Keep code modular and focused, but don't files that aren't needed.
- Prefer editing an existing file to creating a new one.
- You can add README.md files to directories that don't have them, but no other documentation files within the code structure. Docs belong in the `docs/` directory.

## Always Think About Your Context

Codebases like CodeWeaver are, from a token perspective, very large. You become less effective if you try to process many files at once. Take care to only load the files or parts of files that you need to work with, and use narrow searches to get the context you need.

### Avoid these common pitfalls:

- Creating tests, scripts, or using commands that will dump large amounts of data to the console or terminal, unless you design it *not* to return to you. Instead, have it produce a report or summary, or write the output to a file.
  - If you write the output to a file -- *never read it directly*. Instead, use targeted searches to find the information you need.
- Using tools that provide output and don't have a way to limit the output. Always apply filters to reduce the output to only what you need.

Another management strategy is to delegate. If you need to do something with a lot of context -- delegate it to other assistants or tools with detailed instructions on what information you need, how to find it, and how to summarize it for you. This way, you can focus on the high-level tasks and let the tools do the heavy lifting. You need to use the tools effectively to manage your context and avoid overwhelming yourself with too much information at once.
