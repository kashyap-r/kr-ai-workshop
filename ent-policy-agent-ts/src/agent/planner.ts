export interface Plan {
  needsUserContext: boolean;
  needsPolicySearch: boolean;
  needsRefinedSearch: boolean;
  needsApproval: boolean;
  needsAction: boolean;
}