import fs from "fs";
import path from "path";
import { PolicyDocument } from "../types/index.js";

const filePath = path.join(
  process.cwd(),
  "src",
  "data",
  "policies.json"
);

export function loadPolicies(): PolicyDocument[] {
  const raw = fs.readFileSync(filePath, "utf-8");

  return JSON.parse(raw) as PolicyDocument[];
}