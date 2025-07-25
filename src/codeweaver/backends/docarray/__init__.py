# SPDX-FileCopyrightText: 2025 Knitli Inc.
# SPDX-FileContributor: Adam Poulemanos <adam@knit.li>
#
# SPDX-License-Identifier: MIT OR Apache-2.0

"""
DocArray backend integration for CodeWeaver.

Provides unified vector database interface supporting 10+ backends through DocArray,
maintaining full compatibility with CodeWeaver's VectorBackend and HybridSearchBackend protocols.
"""

from .adapter import BaseDocArrayAdapter, DocArrayHybridAdapter
from .config import DocArrayBackendConfig, DocArrayConfigFactory, DocArraySchemaConfig
from .schema import DocumentSchemaGenerator, SchemaConfig, SchemaTemplates


# Re-export main components
__all__ = [
    "BaseDocArrayAdapter",
    "DocArrayBackendConfig",
    "DocArrayConfigFactory",
    "DocArrayHybridAdapter",
    "DocArraySchemaConfig",
    "DocumentSchemaGenerator",
    "SchemaConfig",
    "SchemaTemplates",
]
