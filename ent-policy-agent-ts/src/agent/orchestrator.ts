import OpenAI from "openai";
import { SYSTEM_PROMPT } from "./prompts.js";
import { getUserContext } from "../tools/getUserContext.js";
import { searchPolicies } from "../tools/searchPolicies.js";
import { fileLeaveRequest } from "../tools/fileLeaveRequest.js";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

const tools: OpenAI.Responses.Tool[] = [
  {
    type: "function",
    name: "get_user_context",
    description:
      "Get the employee's context, including department, role, location and employment information.",
    parameters: {
      type: "object",
      properties: {
        userId: {
          type: "string",
          description: "The employee's user ID."
        }
      },
      required: ["userId"],
      additionalProperties: false
    },
    strict: true
  },
  {
    type: "function",
    name: "search_policies",
    description:
      "Search enterprise HR policies and return the most relevant policy information.",
    parameters: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "The policy question or search query."
        }
      },
      required: ["query"],
      additionalProperties: false
    },
    strict: true
  },
  {
    type: "function",
    name: "file_leave_request",
    description:
      "Submit an employee leave request after the agent has determined that the request is allowed.",
    parameters: {
      type: "object",
      properties: {
        userId: {
          type: "string",
          description: "The employee's user ID."
        },
        startDate: {
          type: "string",
          description: "Leave start date in YYYY-MM-DD format."
        },
        endDate: {
          type: "string",
          description: "Leave end date in YYYY-MM-DD format."
        },
        reason: {
          type: "string",
          description: "Reason for the leave request."
        },
        approved: {
          type: "boolean",
          description: "Whether the leave request has been approved."
        }
      },
      required: [
        "userId",
        "startDate",
        "endDate",
        "reason",
        "approved"
      ],
      additionalProperties: false
    },
    strict: true
  }
];

export async function runAgent(userQuery: string) {
  let input: OpenAI.Responses.ResponseInput = [
    {
      role: "user",
      content: userQuery
    }
  ];
// model: "openai/gpt-oss-20b"
// model: "gpt-5.6-luna"
  for (let iteration = 0; iteration < 8; iteration++) {
    const response = await client.responses.create({
      model: "openai/gpt-oss-20b",
      instructions: SYSTEM_PROMPT,
      tools,
      input
    });

    const toolCalls = response.output.filter(
      (item): item is OpenAI.Responses.ResponseFunctionToolCall =>
        item.type === "function_call"
    );

    if (toolCalls.length === 0) {
      return response.output_text;
    }

    for (const call of toolCalls) {
      const args = JSON.parse(call.arguments);

      let result: unknown;

      switch (call.name) {
        case "get_user_context":
          result = await getUserContext(args.userId);
          break;

        case "search_policies":
          result = await searchPolicies(args.query);
          break;

        case "file_leave_request":
          result = await fileLeaveRequest(
            args,
            args.approved
          );
          break;

        default:
          result = {
            error: "Unknown tool"
          };
      }

      input.push(call);

      input.push({
        type: "function_call_output",
        call_id: call.call_id,
        output: JSON.stringify(result)
      });
    }
  }

  throw new Error(
    "Agent exceeded maximum iterations"
  );
}