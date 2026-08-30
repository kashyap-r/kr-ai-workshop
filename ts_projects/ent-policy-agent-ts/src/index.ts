import "dotenv/config";
import { runAgent } from "./agent/orchestrator.js";

const query = `
What's our parental leave policy for contractors
in Sweden, and can you file my request?
`;

const result = await runAgent(query);

console.log("\n==============================");
console.log("AGENT RESPONSE");
console.log("==============================\n");

console.log(result);