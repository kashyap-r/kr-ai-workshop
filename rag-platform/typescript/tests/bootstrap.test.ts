import { describe, expect, it } from "vitest";
import { bootstrapMessage, version } from "../src/index.js";

describe("bootstrap", () => {
  it("exposes the expected package version", () => {
    expect(version).toBe("0.1.0");
  });

  it("returns a health message", () => {
    expect(bootstrapMessage()).toContain("TypeScript environment is ready");
  });
});
