/**
 * Core contracts for the agent runtime.
 *
 * Design note: everything the loop touches is defined here, and nothing here
 * imports from the Anthropic SDK. That keeps the runtime's own vocabulary
 * independent of any one provider's wire format — the adapter that maps to
 * `messages.create` lives in one place and can be swapped.
 */

import type { z } from "zod";

// ---------------------------------------------------------------------------
// Tools
// ---------------------------------------------------------------------------

/**
 * Read-only tools can be retried freely and run without confirmation.
 * Side-effecting tools mutate a real system, so they pass through the
 * human-in-the-loop gate and must never be auto-retried on ambiguous failure.
 */
export type ToolEffect = "read" | "write";

export interface ToolContext {
  /** Correlates every tool call back to the run that issued it. */
  readonly runId: string;
  /** Which iteration of the agent loop we're on (1-indexed). */
  readonly iteration: number;
  /** Aborts in-flight work when the run is cancelled or times out. */
  readonly signal: AbortSignal;
}

/**
 * A tool is a name, a description the model reads, a schema that validates
 * the arguments the model produces, and a function.
 *
 * The schema does double duty: it generates the JSON Schema we send to the
 * model, and it validates at runtime. One source of truth, so the contract
 * the model sees can never drift from the contract we enforce.
 */
export interface Tool<TInput = unknown, TOutput = unknown> {
  readonly name: string;
  readonly description: string;
  readonly effect: ToolEffect;
  readonly schema: z.ZodType<TInput>;
  /** Hard ceiling in ms. A hung tool must not hang the run. */
  readonly timeoutMs?: number;
  /** Rough cap on how many tokens this tool's output may occupy. */
  readonly maxResultTokens?: number;
  execute(input: TInput, ctx: ToolContext): Promise<TOutput>;
}

/** Erased form, for storing heterogeneous tools in one registry. */
export type AnyTool = Tool<any, any>;

// ---------------------------------------------------------------------------
// Tool results
// ---------------------------------------------------------------------------

/**
 * Tool outcomes are values, not exceptions.
 *
 * This matters more than it looks. A failed tool call is not an error the
 * runtime should throw on — it is information the *model* needs, so it can
 * correct its arguments and try again. Throwing would collapse the loop;
 * returning the failure keeps the agent in the conversation.
 */
export type ToolOutcome =
  | { readonly kind: "ok"; readonly content: string; readonly truncated: boolean }
  | { readonly kind: "invalid_args"; readonly message: string }
  | { readonly kind: "failed"; readonly message: string; readonly retryable: boolean }
  | { readonly kind: "timeout"; readonly afterMs: number }
  | { readonly kind: "denied"; readonly reason: string };

export interface ToolCall {
  readonly id: string;
  readonly name: string;
  readonly rawInput: unknown;
}

export interface ToolInvocation {
  readonly call: ToolCall;
  readonly outcome: ToolOutcome;
  readonly durationMs: number;
}

// ---------------------------------------------------------------------------
// Conversation state
// ---------------------------------------------------------------------------

export type Role = "user" | "assistant";

export type ContentBlock =
  | { readonly type: "text"; readonly text: string }
  | { readonly type: "tool_use"; readonly id: string; readonly name: string; readonly input: unknown }
  | {
      readonly type: "tool_result";
      readonly tool_use_id: string;
      readonly content: string;
      readonly is_error: boolean;
    };

export interface Message {
  readonly role: Role;
  readonly content: readonly ContentBlock[];
}

// ---------------------------------------------------------------------------
// Accounting
// ---------------------------------------------------------------------------

/**
 * Cache reads and writes are tracked separately because they are priced
 * differently. Collapsing them into one `inputTokens` number is the single
 * easiest way to lose the ability to tell whether caching is working.
 */
export interface TokenUsage {
  readonly inputTokens: number;
  readonly outputTokens: number;
  readonly cacheCreationTokens: number;
  readonly cacheReadTokens: number;
}

export interface StepRecord {
  readonly iteration: number;
  readonly usage: TokenUsage;
  readonly costUsd: number;
  readonly latencyMs: number;
  readonly toolCalls: readonly ToolInvocation[];
}

// ---------------------------------------------------------------------------
// Run outcome
// ---------------------------------------------------------------------------

/**
 * Why the loop stopped. Every one of these except "answered" is a defence
 * firing, and each is counted separately so a regression in any one of them
 * shows up in the evals rather than hiding inside a generic failure rate.
 */
export type StopReason =
  | "answered"
  | "iteration_cap"
  | "loop_detected"
  | "budget_exhausted"
  | "awaiting_approval"
  | "model_error"
  | "aborted";

export interface RunResult {
  readonly runId: string;
  readonly stopReason: StopReason;
  /** Populated when stopReason is "answered", or when we degraded gracefully. */
  readonly answer: string | null;
  /** True when `answer` came from a fallback path rather than a clean finish. */
  readonly degraded: boolean;
  readonly messages: readonly Message[];
  readonly steps: readonly StepRecord[];
  readonly totalUsage: TokenUsage;
  readonly totalCostUsd: number;
  readonly totalLatencyMs: number;
}

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

export interface RunLimits {
  /** Hard ceiling on loop iterations. The primary non-termination defence. */
  readonly maxIterations: number;
  /** Abandon the run above this spend. The primary cost defence. */
  readonly maxCostUsd: number;
  /** Wall-clock ceiling for the whole run. */
  readonly maxWallClockMs: number;
  /** Identical (tool, args) pairs seen this many times ⇒ loop_detected. */
  readonly repeatCallThreshold: number;
}

export interface ContextBudget {
  /** Total prompt tokens we are willing to send on any single turn. */
  readonly totalTokens: number;
  /** Reserved for the system prompt. Never truncated. */
  readonly systemTokens: number;
  /** Reserved for tool definitions. Never truncated. */
  readonly toolDefinitionTokens: number;
  /** Reserved for the model's reply. */
  readonly responseTokens: number;
  /** What remains is history; older turns are summarised out to fit. */
}

export const DEFAULT_LIMITS: RunLimits = {
  maxIterations: 12,
  maxCostUsd: 0.5,
  maxWallClockMs: 120_000,
  repeatCallThreshold: 3,
};

export const DEFAULT_BUDGET: ContextBudget = {
  totalTokens: 100_000,
  systemTokens: 2_000,
  toolDefinitionTokens: 3_000,
  responseTokens: 4_000,
};
