import { loadPolicies } from "../retrieval/retriever.js";
import { lexicalSearch } from "../retrieval/lexical.js";
import { rerank } from "../retrieval/ranker.js";
import { UserContext } from "../types/index.js";

export async function searchPolicies(
  query: string,
  context?: UserContext
) {

  const documents = loadPolicies();

  const lexicalResults =
    lexicalSearch(query, documents);

  const reranked =
    rerank(lexicalResults, context);

  return reranked.slice(0, 5);
}