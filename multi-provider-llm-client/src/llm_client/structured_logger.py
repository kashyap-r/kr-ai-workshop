import json
import logging
from datetime import datetime, timezone

from .metrics import LLMMetrics


logger = logging.getLogger(
    "llm_client"
)


class StructuredLogger:

    def __init__(self):

        self.logger = logger

    def log_metrics(
        self,
        metrics: LLMMetrics,
    ) -> None:

        event = {
            "event": "llm_request",

            "timestamp": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),

            "request_id": (
                metrics.request_id
            ),

            "provider": (
                metrics.provider
            ),

            "model": (
                metrics.model
            ),

            "latency_ms": (
                metrics.latency_ms
            ),

            "attempts": (
                metrics.attempts
            ),

            "retry_count": (
                metrics.retry_count
            ),

            "retry_delay_ms": (
                metrics.retry_delay_ms
            ),

            "input_tokens": (
                metrics.usage.input_tokens
                if metrics.usage
                else None
            ),

            "output_tokens": (
                metrics.usage.output_tokens
                if metrics.usage
                else None
            ),

            "total_tokens": (
                metrics.usage.total_tokens
                if metrics.usage
                else None
            ),

            "success": (
                metrics.success
            ),

            "error_type": (
                metrics.error_type
            ),

            "error_message": (
                metrics.error_message
            ),
        }

        self.logger.info(
            json.dumps(
                event,
                default=str,
            )
        )

    def log_retry_event(
        self,
        event_type: str,
        data: dict,
    ) -> None:

        event = {
            "event": event_type,

            "timestamp": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),

            **data,
        }

        self.logger.info(
            json.dumps(
                event,
                default=str,
            )
        )