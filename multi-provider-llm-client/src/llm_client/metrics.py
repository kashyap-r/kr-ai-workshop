"""
Author: Kashyap R
Date: 18th Aug, 2026
"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class LLMUsage:
    input_tokens: int | None = None 
    output_tokens: int | None = None 
    total_tokens: int | None = None 

@dataclass
class LLMMetrics:
    request_id: str
    provider: str
    model: str
    start_time: datetime
    end_time: datetime | None = None
    latency_ms: float | None = None
    attempts: int = 1
    retry_count: int = 0
    retry_delay_ms: float = 0.0
    success: bool = False
    error_type: str | None = None
    error_message: str | None = None
    usage: LLMUsage | None = None