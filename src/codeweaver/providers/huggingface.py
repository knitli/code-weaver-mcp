# SPDX-FileCopyrightText: 2025 Knitli Inc.
# SPDX-FileContributor: Adam Poulemanos <adam@knit.li>
#
# SPDX-License-Identifier: MIT OR Apache-2.0

"""
HuggingFace provider implementation for embeddings.

Provides HuggingFace Inference API and local transformers models using the unified provider interface.
Supports both cloud inference and local model loading with GPU acceleration.
"""

import logging

from typing import Any

from codeweaver._types import (
    EmbeddingProviderInfo,
    ProviderCapability,
    ProviderType,
    get_provider_registry_entry,
    register_provider_class,
)
from codeweaver.providers.base import EmbeddingProviderBase
from codeweaver.providers.config import HuggingFaceConfig


try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

try:
    import torch
    import transformers

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    transformers = None
    torch = None


logger = logging.getLogger(__name__)


class HuggingFaceProvider(EmbeddingProviderBase):
    """HuggingFace provider for embeddings with support for API and local models."""

    def __init__(self, config: dict[str, Any] | HuggingFaceConfig):
        """Initialize HuggingFace provider.

        Args:
            config: Configuration dictionary or HuggingFaceConfig instance with settings for:
                - model: Model name
                - api_key: HuggingFace API key (optional for public models)
                - use_local: Whether to use local model loading
                - device: Device for local models ('cpu', 'cuda', 'auto')
                - batch_size: Batch size for local processing
        """
        super().__init__(config)

        # Get registry entry for validation and defaults
        self._registry_entry = get_provider_registry_entry(ProviderType.HUGGINGFACE)

        # Convert to Pydantic config if needed
        if isinstance(config, dict):
            # Set model default from registry if not provided
            if "model" not in config:
                config["model"] = self._registry_entry.capabilities.default_embedding_model
            self._config = HuggingFaceConfig(**config)
        else:
            self._config = config

        # Validate model is supported
        if self._config.model not in self._registry_entry.capabilities.supported_embedding_models:
            logger.warning(
                "Model %s not in known supported models. May work but not guaranteed.",
                self._config.model,
            )

        # Configuration
        self._model_name = self._config.model
        self._api_key = self._config.api_key
        self._use_local = getattr(self._config, "use_local", False)
        self._device = getattr(self._config, "device", "auto")
        self._batch_size = self._config.batch_size

        # Initialize based on mode
        if self._use_local:
            self._init_local_model()
        else:
            self._init_api_client()

        # Get dimension from registry or estimate
        self._dimension = self._registry_entry.capabilities.native_dimensions.get(
            self._model_name, 768
        )

    def _validate_config(self) -> None:
        """Validate HuggingFace configuration."""
        if self._use_local and not TRANSFORMERS_AVAILABLE:
            raise ValueError(
                "Local model mode requires transformers. Install with: uv add transformers torch"
            )

        if not self._use_local and not REQUESTS_AVAILABLE:
            raise ValueError("API mode requires requests. Install with: uv add requests")

        if not self._use_local and not self._api_key:
            logger.warning(
                "No HuggingFace API key provided. Rate limits will apply for public inference."
            )

    def _init_local_model(self) -> None:  # sourcery skip: avoid-global-variables, extract-method
        """Initialize local transformers model."""
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("transformers and torch required for local models")

        try:
            from transformers import AutoModel, AutoTokenizer

            self._tokenizer = AutoTokenizer.from_pretrained(self._model_name)
            self._model = AutoModel.from_pretrained(self._model_name)

            # Move to device
            if self._device == "auto":
                self._device = "cuda" if torch.cuda.is_available() else "cpu"
            self._model.to(self._device)

            logger.info("Loaded local HuggingFace model: %s on %s", self._model_name, self._device)

        except Exception as e:
            raise RuntimeError(f"Failed to load local model {self._model_name}: {e}") from e

    def _init_api_client(self) -> None:
        """Initialize API client for HuggingFace Inference API."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests required for HuggingFace API")

        self._api_url = (
            f"https://api-inference.huggingface.co/pipeline/feature-extraction/{self._model_name}"
        )
        self._headers = {}

        if self._api_key:
            self._headers["Authorization"] = f"Bearer {self._api_key}"

        logger.info("Initialized HuggingFace API client for: %s", self._model_name)

    # EmbeddingProvider implementation

    @property
    def provider_name(self) -> str:
        """Get the provider name."""
        return ProviderType.HUGGINGFACE.value

    @property
    def model_name(self) -> str:
        """Get the current model name."""
        return self._model_name

    @property
    def dimension(self) -> int:
        """Get the embedding dimension."""
        return self._dimension

    @property
    def max_batch_size(self) -> int | None:
        """Batch size depends on mode."""
        return self._batch_size if self._use_local else 1

    @property
    def max_input_length(self) -> int | None:
        """Input length depends on model tokenizer limits."""
        return 8000  # Conservative estimate for most models

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for documents."""
        try:
            if self._use_local:
                return await self._embed_local(texts)
            return await self._embed_api(texts)
        except Exception:
            logger.exception("Error generating HuggingFace embeddings")
            raise

    async def embed_query(self, text: str) -> list[float]:
        """Generate embedding for search query."""
        try:
            embeddings = await self.embed_documents([text])
            return embeddings[0]
        except Exception:
            logger.exception("Error generating HuggingFace query embedding")
            raise

    async def _embed_local(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings using local model."""
        if not TRANSFORMERS_AVAILABLE:
            raise RuntimeError("Local model not available")

        import torch

        embeddings = []

        # Process in batches
        for i in range(0, len(texts), self._batch_size):
            batch_texts = texts[i : i + self._batch_size]

            # Tokenize
            encoded = self._tokenizer(
                batch_texts, padding=True, truncation=True, return_tensors="pt", max_length=512
            )

            # Move to device
            encoded = {k: v.to(self._device) for k, v in encoded.items()}

            # Generate embeddings
            with torch.no_grad():
                outputs = self._model(**encoded)

                # Use mean pooling of last hidden states
                attention_mask = encoded["attention_mask"]
                token_embeddings = outputs.last_hidden_state

                # Mean pooling
                input_mask_expanded = (
                    attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
                )
                batch_embeddings = torch.sum(
                    token_embeddings * input_mask_expanded, 1
                ) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

                # Normalize
                batch_embeddings = torch.nn.functional.normalize(batch_embeddings, p=2, dim=1)

                # Convert to list
                batch_embeddings = batch_embeddings.cpu().numpy().tolist()
                embeddings.extend(batch_embeddings)

        return embeddings

    async def _embed_api(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings using HuggingFace Inference API."""
        if not REQUESTS_AVAILABLE:
            raise RuntimeError("API client not available")

        embeddings = []

        for text in texts:
            response = requests.post(
                self._api_url, headers=self._headers, json={"inputs": text}, timeout=30
            )

            if response.status_code != 200:
                raise RuntimeError(
                    f"HuggingFace API error: {response.status_code} - {response.text}"
                )

            embedding = response.json()

            # Handle different response formats
            if isinstance(embedding, list) and isinstance(embedding[0], list):
                # Already in correct format
                embeddings.append(embedding[0])
            elif isinstance(embedding, list):
                # Single embedding vector
                embeddings.append(embedding)
            else:
                raise TypeError(f"Unexpected API response format: {type(embedding)}")

        return embeddings

    # Provider info methods

    def get_provider_info(self) -> EmbeddingProviderInfo:
        """Get information about HuggingFace capabilities from centralized registry."""
        capabilities = self._registry_entry.capabilities

        return EmbeddingProviderInfo(
            name=ProviderType.HUGGINGFACE.value,
            display_name=self._registry_entry.display_name,
            description=self._registry_entry.description,
            supported_capabilities=[
                ProviderCapability.EMBEDDING,
                ProviderCapability.LOCAL_INFERENCE,
                ProviderCapability.BATCH_PROCESSING,
            ],
            capabilities=capabilities,
            default_models={"embedding": capabilities.default_embedding_model},
            supported_models={"embedding": capabilities.supported_embedding_models},
            rate_limits={
                "requests_per_minute": capabilities.requests_per_minute,
                "tokens_per_minute": capabilities.tokens_per_minute,
            },
            requires_api_key=capabilities.requires_api_key,
            max_batch_size=capabilities.max_batch_size,
            max_input_length=capabilities.max_input_length,
            native_dimensions=capabilities.native_dimensions,
        )

    @classmethod
    def get_static_provider_info(cls) -> EmbeddingProviderInfo:
        """Get static provider information from centralized registry."""
        registry_entry = get_provider_registry_entry(ProviderType.HUGGINGFACE)
        capabilities = registry_entry.capabilities

        return EmbeddingProviderInfo(
            name=ProviderType.HUGGINGFACE.value,
            display_name=registry_entry.display_name,
            description=registry_entry.description,
            supported_capabilities=[
                ProviderCapability.EMBEDDING,
                ProviderCapability.LOCAL_INFERENCE,
                ProviderCapability.BATCH_PROCESSING,
            ],
            capabilities=capabilities,
            default_models={"embedding": capabilities.default_embedding_model},
            supported_models={"embedding": capabilities.supported_embedding_models},
            rate_limits={
                "requests_per_minute": capabilities.requests_per_minute,
                "tokens_per_minute": capabilities.tokens_per_minute,
            },
            requires_api_key=capabilities.requires_api_key,
            max_batch_size=capabilities.max_batch_size,
            max_input_length=capabilities.max_input_length,
            native_dimensions=capabilities.native_dimensions,
        )

    @classmethod
    def check_availability(cls, capability: ProviderCapability) -> tuple[bool, str | None]:
        """Check if HuggingFace is available for the given capability."""
        # Check for API mode
        if not REQUESTS_AVAILABLE:
            api_available = False
            api_reason = "requests package not installed"
        else:
            api_available = True
            api_reason = None

        # Check for local mode
        if not TRANSFORMERS_AVAILABLE:
            local_available = False
            local_reason = "transformers/torch packages not installed"
        else:
            local_available = True
            local_reason = None

        # Handle different capabilities
        if capability == ProviderCapability.EMBEDDING:
            if api_available or local_available:
                return True, None
            return (False, f"Neither API ({api_reason}) nor local ({local_reason}) mode available")

        if capability == ProviderCapability.LOCAL_INFERENCE:
            return (True, None) if local_available else (False, local_reason)
        if capability == ProviderCapability.BATCH_PROCESSING:
            # Batch processing is always available if embedding is available
            if api_available or local_available:
                return True, None
            return (False, f"Neither API ({api_reason}) nor local ({local_reason}) mode available")

        return False, f"Capability {capability.value} not supported by HuggingFace"


# Register the HuggingFace provider in the registry
register_provider_class(ProviderType.HUGGINGFACE, HuggingFaceProvider)
