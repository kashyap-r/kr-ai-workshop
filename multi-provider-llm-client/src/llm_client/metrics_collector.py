from .metrics import LLMMetrics
from .structured_logger import StructuredLogger
from .request_context import (
    get_request_context,
)


class MetricsCollector:

    def __init__(
        self,
        logger: StructuredLogger | None = None,
    ):

        self.logger = (
            logger
            if logger
            else StructuredLogger()
        )

    def record(
        self,
        metrics: LLMMetrics,
    ) -> None:

        self.logger.log_metrics(
            metrics
        )

    def record_retry_event(
        self,
        event_type: str,
        data: dict,
    ) -> None:

        context = get_request_context()

        event_data = dict(data)

        if context:

            event_data[
                "request_id"
            ] = context.request_id

        self.logger.log_retry_event(
            event_type,
            event_data,
        )