import time
import uuid
from datetime import datetime, timezone

from .base import LLMClient, LLMResponse
from .errors import LLMError
from .metrics import LLMMetrics
from .metrics_collector import MetricsCollector
from .request_context import (
    RequestContext,
    set_request_context,
    reset_request_context,
)


class MetricsLLMClient(LLMClient):

    def __init__(
        self,
        client: LLMClient,
        collector: MetricsCollector,
    ):
        self.client = client
        self.collector = collector

    def retry_event(
        self,
        event_type: str,
        data: dict,
    ) -> None:

        self.collector.record_retry_event(
            event_type,
            data,
        )

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        request_id = str(
            uuid.uuid4()
        )

        context = RequestContext(
            request_id=request_id
        )

        context_token = (
            set_request_context(
                context
            )
        )

        start_time = datetime.now(
            timezone.utc
        )

        start_perf = time.perf_counter()

        try:

            response = self.client.generate(
                prompt
            )

            end_perf = time.perf_counter()

            end_time = datetime.now(
                timezone.utc
            )

            metrics = LLMMetrics(
                request_id=request_id,
                provider=response.provider,
                model=response.model,
                start_time=start_time,
                end_time=end_time,
                latency_ms=(
                    end_perf - start_perf
                ) * 1000,
                attempts=(
                    context.attempts
                    or 1
                ),
                retry_count=(
                    context.retry_count
                ),
                retry_delay_ms=(
                    context.retry_delay_seconds
                    * 1000
                ),
                success=True,
                usage=response.usage,
            )

            response.metrics = metrics

            self.collector.record(
                metrics
            )

            return response

        except LLMError as e:

            end_perf = time.perf_counter()

            end_time = datetime.now(
                timezone.utc
            )

            metrics = LLMMetrics(
                request_id=request_id,
                provider="unknown",
                model="unknown",
                start_time=start_time,
                end_time=end_time,
                latency_ms=(
                    end_perf - start_perf
                ) * 1000,
                attempts=(
                    context.attempts
                    or 1
                ),
                retry_count=(
                    context.retry_count
                ),
                retry_delay_ms=(
                    context.retry_delay_seconds
                    * 1000
                ),
                success=False,
                error_type=type(e).__name__,
                error_message=str(e),
            )

            self.collector.record(
                metrics
            )

            raise

        finally:

            reset_request_context(
                context_token
            )