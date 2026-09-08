NOTE: Eventually the evaluation framework should replace this 

Run these from the repo root:
1. See how many chunk artifacts were produced
Run: find data/processed/chunks/ZCompanyLLC -name "*.jsonl" | wc -l

2. Count total Chunks 
Run: wc -l $(find data/processed/chunks/ZCompanyLLC -name "*.jsonl")
This will show the number of chunks in each file plus a total.

3. 3. Inspect one chunk file

Pick something representative:
cat data/processed/chunks/ZCompanyLLC/sweden/policies/sweden_leave_policy.jsonl