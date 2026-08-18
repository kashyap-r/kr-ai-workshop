from datetime import datetime, timezone

from llm_client.metrics import (
    LLMUsage,
    LLMMetrics,
)
from llm_client.structured_logger import (
    StructuredLogger,
)


metrics = LLMMetrics(
    request_id="test-123",
    provider="groq",
    model="Qwen/Qwen3.6-27B",
    start_time=datetime.now(
        timezone.utc
    ),
    latency_ms=250.5,
    attempts=1,
    retry_count=0,
    retry_delay_ms=0.0,
    success=True,
    usage=LLMUsage(
        input_tokens=10,
        output_tokens=20,
        total_tokens=30,
    ),
)


logger = StructuredLogger()

logger.log_metrics(metrics)