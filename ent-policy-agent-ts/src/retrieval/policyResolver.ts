import { SearchResult } from "../types/index.js";

export function resolvePolicyVersions(
  results: SearchResult[]
): SearchResult[] {

  const grouped =
    new Map<string, SearchResult[]>();

  for (const result of results) {

    const title =
      result.document.title;

    if (!grouped.has(title)) {
      grouped.set(title, []);
    }

    grouped.get(title)!.push(result);
  }

  const resolved: SearchResult[] = [];

  for (const [, documents] of grouped) {

    documents.sort(
      (a, b) =>
        new Date(
          b.document.effectiveDate
        ).getTime()
        -
        new Date(
          a.document.effectiveDate
        ).getTime()
    );

    resolved.push(documents[0]);
  }

  return resolved;
}