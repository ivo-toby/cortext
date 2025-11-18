"""Embedding generation using fastembed."""

from typing import Any


class Embedder:
    """Generate embeddings using fastembed (lightweight, no PyTorch)."""

    # Model name mapping for convenience
    MODEL_ALIASES = {
        "all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2",
    }

    # Known embedding dimensions
    MODEL_DIMENSIONS = {
        "sentence-transformers/all-MiniLM-L6-v2": 384,
    }

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedder with lazy model loading."""
        # Support both short and full names
        self._model_name = self.MODEL_ALIASES.get(model_name, model_name)
        self._model = None
        self._embedding_dim = self.MODEL_DIMENSIONS.get(self._model_name)

    @property
    def model_name(self) -> str:
        """Get model name."""
        return self._model_name

    @property
    def embedding_dim(self) -> int:
        """Get embedding dimension (loads model if needed)."""
        if self._embedding_dim is None:
            self._load_model()
        return self._embedding_dim

    def _load_model(self) -> None:
        """Load model lazily on first use."""
        if self._model is not None:
            return

        from fastembed import TextEmbedding

        self._model = TextEmbedding(model_name=self._model_name)

        # If dimension not known, get it from a test embedding
        if self._embedding_dim is None:
            test_emb = list(self._model.embed(["test"]))[0]
            self._embedding_dim = len(test_emb)

    def embed(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of text strings to embed
            batch_size: Batch size for processing (default 32)

        Returns:
            List of embedding vectors (each vector is list of floats)
        """
        if not texts:
            return []

        self._load_model()

        # fastembed returns a generator of numpy arrays
        embeddings = list(self._model.embed(texts, batch_size=batch_size))

        # Convert to list of lists for JSON serialization
        return [emb.tolist() for emb in embeddings]

    def embed_single(self, text: str) -> list[float]:
        """Generate embedding for single text.

        Args:
            text: Text string to embed

        Returns:
            Embedding vector as list of floats
        """
        return self.embed([text])[0]

    def get_metadata(self) -> dict[str, Any]:
        """Get model metadata."""
        return {
            "model_name": self.model_name,
            "embedding_dim": self.embedding_dim,
        }
