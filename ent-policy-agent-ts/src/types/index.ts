/*
Authore: Kashyap R
Description: Definitions for the enterprise document model. 
*/

export type EmployeeType =
  | "employee"
  | "contractor"
  | "all";

export interface PolicyDocument {
  id: string;
  title: string;
  source: "confluence" | "notion" | "google_drive" | "hr_system";
  version: string;
  effectiveDate: string;
  country?: string;
  employeeType: EmployeeType;
  content: string;
}

export interface SearchResult {
  document: PolicyDocument;
  score: number;
  semanticScore: number;
  lexicalScore: number;
}

export interface UserContext {
  userId: string;
  country: string;
  employeeType: EmployeeType;
  employmentStartDate: string;
}

export interface LeaveRequest {
  leaveType: string;
  startDate: string;
  endDate: string;
  reason?: string;
}

export interface AgentState {
  userQuery: string;
  userContext?: UserContext;
  searchResults: SearchResult[];
  approvalRequired: boolean;
  actionExecuted: boolean;
}

/**
 * Questions
 * 1. Why export type, and export interface ?
 * 2. What is the difference between the two
 */