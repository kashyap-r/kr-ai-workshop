import { AgentState } from "../types/index.js";

export function createInitialState(
  userQuery: string
): AgentState {

  return {
    userQuery,
    searchResults: [],
    approvalRequired: false,
    actionExecuted: false
  };
}