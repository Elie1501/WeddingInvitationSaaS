# Limiteur de débit minimal, en mémoire (par process). Suffisant pour freiner
# le brute-force (login) et le spam (RSVP public) en mono-instance. Pour du
# multi-worker/horizontal, remplacer par un store partagé (Redis).

import time
from collections import defaultdict
from fastapi import Request, HTTPException, status

_hits = defaultdict(list)  # "scope:ip" -> [timestamps]


def rate_limit(request: Request, *, scope: str, limit: int, window_seconds: int) -> None:
    now = time.time()
    ip = request.client.host if request.client else "unknown"
    bucket = f"{scope}:{ip}"
    recent = [t for t in _hits[bucket] if now - t < window_seconds]
    if len(recent) >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Trop de tentatives. Veuillez réessayer dans quelques minutes.",
        )
    recent.append(now)
    _hits[bucket] = recent
