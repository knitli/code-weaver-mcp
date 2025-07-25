# SPDX-FileCopyrightText: 2025 Knitli Inc.
# SPDX-FileContributor: Adam Poulemanos <adam@knit.li>
#
# SPDX-License-Identifier: MIT OR Apache-2.0

"""
Vector database backends for CodeWeaver.

This module provides comprehensive abstractions for 15+ vector databases
with support for hybrid search, streaming operations, and transactions.
"""

from codeweaver._types import (
    CollectionInfo,
    DistanceMetric,
    FilterCondition,
    SearchResult,
    VectorPoint,
)
from codeweaver._types.exceptions import (
    BackendAuthError,
    BackendCollectionNotFoundError,
    BackendConnectionError,
    BackendError,
    BackendUnsupportedOperationError,
    BackendVectorDimensionMismatchError,
)
from codeweaver.backends.base import (
    HybridSearchBackend,
    StreamingBackend,
    TransactionalBackend,
    VectorBackend,
)
from codeweaver.backends.config import (
    EXAMPLE_CONFIGS,
    BackendConfigExtended,
    create_backend_config_from_env,
    get_provider_specific_config,
)
from codeweaver.backends.factory import BackendConfig, BackendFactory
from codeweaver.backends.qdrant import QdrantBackend, QdrantHybridBackend


# Try to import DocArray backends (optional)
try:
    from codeweaver.backends.docarray import factory as docarray_factory  # noqa: F401

    _DOCARRAY_AVAILABLE = True
except ImportError:
    _DOCARRAY_AVAILABLE = False


__all__ = [
    "EXAMPLE_CONFIGS",
    "BackendAuthError",
    "BackendCollectionNotFoundError",
    # Configuration
    "BackendConfig",
    "BackendConfigExtended",
    "BackendConnectionError",
    # Exceptions
    "BackendError",
    # Factory
    "BackendFactory",
    # Enums
    "BackendUnsupportedOperationError",
    "BackendVectorDimensionMismatchError",
    "CollectionInfo",
    "DistanceMetric",
    "FilterCondition",
    "HybridSearchBackend",
    # Implementations
    "QdrantBackend",
    "QdrantHybridBackend",
    "SearchResult",
    "StreamingBackend",
    "TransactionalBackend",
    # Core protocols
    "VectorBackend",
    # Data structures
    "VectorPoint",
    "create_backend_config_from_env",
    "get_provider_specific_config",
]
