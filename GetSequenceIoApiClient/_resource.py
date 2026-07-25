from __future__ import annotations

from typing import TypeVar

from ._base import BaseClient
from ._types import JsonObject, QueryParams

ModelT = TypeVar("ModelT")


class BaseResource:
    """Typed helpers shared by resource/service classes."""

    def __init__(self, base: BaseClient) -> None:
        self._base = base

    def _url(self, path: str) -> str:
        return f"{self._base.base_url}/{path.lstrip('/')}"

    async def _list_items(
        self,
        *,
        path: str,
        params: QueryParams,
        page: int | None,
        item_model: type[ModelT],
    ) -> list[ModelT]:
        url = self._url(path)
        if page is not None:
            data = await self._base._async_request("GET", url, params=params)
            items = data.get("items", []) if isinstance(data, dict) else []
        else:
            items = await self._base._async_get_all_pages(url, params)

        if not all(isinstance(item, dict) for item in items):
            raise TypeError(f"Expected item dictionaries for resource path '{path}'")

        return [item_model.from_dict(item) for item in items]
