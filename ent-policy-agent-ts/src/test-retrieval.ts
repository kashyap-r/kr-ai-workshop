import "dotenv/config";

import { loadPolicies } from "./retrieval/retriever.js";
import { lexicalSearch } from "./retrieval/lexical.js";

const query = "parental leave contractor Sweden";

const documents = loadPolicies();

console.log(`Loaded ${documents.length} documents\n`);

const results = lexicalSearch(query, documents);

console.log("SEARCH RESULTS");
console.log("==============================");

for (const result of results) {
  console.log("\nDocument:", result.document.id);
  console.log("Title:", result.document.title);
  console.log("Country:", result.document.country ?? "Global");
  console.log("Employee Type:", result.document.employeeType);
  console.log("Version:", result.document.version);
  console.log("Score:", result.score.toFixed(3));
}