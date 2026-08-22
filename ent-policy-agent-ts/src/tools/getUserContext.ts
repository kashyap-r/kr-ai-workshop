import { UserContext } from "../types/index.js";

export async function getUserContext(
  userId: string
): Promise<UserContext> {

  // Mock HR system
  return {
    userId,
    country: "Sweden",
    employeeType: "contractor",
    employmentStartDate: "2026-01-15"
  };
}