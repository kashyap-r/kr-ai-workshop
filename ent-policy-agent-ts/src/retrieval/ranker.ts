import {
  PolicyDocument,
  SearchResult,
  UserContext
} from "../types/index.js";

export function metadataScore(
  document: PolicyDocument,
  context?: UserContext
): number {

  if (!context) {
    return 0;
  }

  let score = 0;

  if (
    document.country &&
    document.country.toLowerCase() ===
      context.country.toLowerCase()
  ) {
    score += 0.5;
  }

  if (
    document.employeeType === context.employeeType ||
    document.employeeType === "all"
  ) {
    score += 0.5;
  }

  return Math.min(score, 1);
}

export function rerank(
  results: SearchResult[],
  context?: UserContext
): SearchResult[] {

  return results
    .map((result) => {

      const meta = metadataScore(
        result.document,
        context
      );

      const score =
        0.5 * result.semanticScore +
        0.3 * result.lexicalScore +
        0.2 * meta;

      return {
        ...result,
        score
      };
    })
    .sort((a, b) => b.score - a.score);
}