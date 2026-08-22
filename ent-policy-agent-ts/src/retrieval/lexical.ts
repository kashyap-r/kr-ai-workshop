import { PolicyDocument, SearchResult } from "../types/index.js";

function tokenize(text: string): string[] {
  return text
    .toLowerCase()
    .split(/\W+/)
    .filter(Boolean);
}

export function lexicalSearch(
  query: string,
  documents: PolicyDocument[]
): SearchResult[] {

  const queryTokens = tokenize(query);

  return documents
    .map((document) => {

      const documentText = `
        ${document.title}
        ${document.country ?? ""}
        ${document.employeeType}
        ${document.content}
      `;

      const documentTokens = tokenize(documentText);

      const matches = queryTokens.filter((token) =>
        documentTokens.includes(token)
      );

      const score =
        matches.length / Math.max(queryTokens.length, 1);

      return {
        document,
        score,
        semanticScore: 0,
        lexicalScore: score
      };
    })
    .filter((result) => result.score > 0)
    .sort((a, b) => b.score - a.score);
}