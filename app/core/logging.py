"""Structured logging setup using `structlog`.

The pipeline logs the metrics called out in the project goal: number of loaded
documents, number of generated chunks, embedding time, indexing time, failed
files, and the Qdrant collection status. Structured logs make those metrics
easy to read locally and easy to parse in production.
"""

from __future__ import annotations

import logging
import sys

import structlog


def configure_logging(level: str = "INFO") -> None:
    """Configure standard logging and structlog to emit readable, structured logs.

    Call this once at application startup (API and CLI both do this).
    """
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, level.upper(), logging.INFO),
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper(), logging.INFO)
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Return a structured logger, optionally bound to a component name."""
    return structlog.get_logger(name)
