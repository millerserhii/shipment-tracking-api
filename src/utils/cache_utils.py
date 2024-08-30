import logging
from typing import Any, Optional

from django.core.cache import cache


logger = logging.getLogger("main")
CACHE_TTL = 60 * 60 * 2  # 2 hours


def delete_cache(key_prefix: str) -> None:
    try:
        cache.delete_pattern(f"*{key_prefix}*")  # type: ignore[attr-defined]
        logger.debug("Cache with key prefix %s deleted", key_prefix)
    except AttributeError:
        logger.warning(
            "Skipping cache deletion for key prefix %s in test environment",
            key_prefix,
        )


def get_cached_weather(
    postal_code: str, country: str
) -> Optional[dict[str, Any]]:
    cache_key: str = f"weather_{postal_code}_{country}"
    return cache.get(cache_key)


def set_cached_weather(
    postal_code: str, country: str, data: dict[str, Any], ttl: int = CACHE_TTL
) -> None:
    cache_key: str = f"weather_{postal_code}_{country}"
    cache.set(cache_key, data, ttl)
