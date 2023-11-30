from typing import Callable, List, Optional

from redisvl.utils.utils import array_to_buffer


class BaseVectorizer:
    _dims = None

    def __init__(self, model: str):
        self._model = model

    @property
    def model(self) -> str:
        return self._model

    @property
    def dims(self) -> Optional[int]:
        return self._dims

    def set_model(self, model: str, dims: Optional[int] = None) -> None:
        self._model = model
        if dims is not None:
            self._dims = dims

    def embed_many(
        self,
        texts: List[str],
        preprocess: Optional[Callable] = None,
        batch_size: int = 1000,
        as_buffer: bool = False,
    ) -> List[List[float]]:
        raise NotImplementedError

    def embed(
        self,
        text: str,
        preprocess: Optional[Callable] = None,
        as_buffer: bool = False,
    ) -> List[float]:
        raise NotImplementedError

    async def aembed_many(
        self,
        texts: List[str],
        preprocess: Optional[Callable] = None,
        batch_size: int = 1000,
        as_buffer: bool = False,
    ) -> List[List[float]]:
        raise NotImplementedError

    async def aembed(
        self,
        text: str,
        preprocess: Optional[Callable] = None,
        as_buffer: bool = False,
    ) -> List[float]:
        raise NotImplementedError

    def batchify(self, seq: list, size: int, preprocess: Optional[Callable] = None):
        for pos in range(0, len(seq), size):
            if preprocess is not None:
                yield [preprocess(chunk) for chunk in seq[pos : pos + size]]
            else:
                yield seq[pos : pos + size]

    def _process_embedding(self, embedding: List[float], as_buffer: bool):
        return array_to_buffer(embedding) if as_buffer else embedding
