"""Embedding generation using sentence-transformers."""

from typing import Any


class Embedder:
    """Generate embeddings using sentence-transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedder with lazy model loading."""
        self._model_name = model_name
        self._model = None
        self._embedding_dim = None

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

        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers not installed. "
                "Install with: pip install cortext-workspace[rag]"
            )

        self._model = SentenceTransformer(self._model_name)
        # Get embedding dimension from model
        self._embedding_dim = self._model.get_sentence_embedding_dimension()

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

        # Encode with batching
        embeddings = self._model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=len(texts) > 100,
            convert_to_numpy=True,
        )

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
