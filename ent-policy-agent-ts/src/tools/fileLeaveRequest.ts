import { LeaveRequest } from "../types/index.js";

export async function fileLeaveRequest(
  request: LeaveRequest,
  approved: boolean
) {

  if (!approved) {
    return {
      success: false,
      status: "APPROVAL_REQUIRED",
      message:
        "User approval is required before filing the leave request."
    };
  }

  // Mock side effect
  const ticketId =
    `HR-${Math.floor(Math.random() * 100000)}`;

  return {
    success: true,
    status: "SUBMITTED",
    ticketId,
    request
  };
}