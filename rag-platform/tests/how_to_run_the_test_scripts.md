From the project root folder: To run all the tests
Run: uv run pytest 

uv run pytest tests/retrieval tests/query

To run the tests after API changes 
uv run pytest tests/retrieval tests/query tests/api

-----------------------

Running the COntext Builder Pipeline 

uv run pytest
uv run mypy src/rag_platform
uv run ruff check src tests


----------------------------

query Context E2E Test 

uv run uvicorn rag_platform.api:app --reload

In another terminal window: 

curl -s \
  -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: m10-4-test-001" \
  -d '{
    "query": "What is the company'\''s policy for working from home?",
    "top_k": 5
  }' | python -m json.tool


Run validation in this order

First:

uv run pytest tests/query/test_service.py -v

Then your API tests:

uv run pytest tests -k "api" -v

Then context tests:

uv run pytest tests/context -v

Then full regression:

uv run pytest

Then:

uv run mypy src/rag_platform

Then:

uv run ruff check src tests

Finally:

uv run uvicorn api:app --reload

and the curl test above.



Note: Just to test the one script 
ex. uv run pytest tests/api/test_api.py -v


----------------------

That's just your shell environment: your project uses uv/Python, but there is no python executable on your PATH.

Use:

uv run python -m json.tool

So rerun the curl command as:

curl -s \
  -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: m10-4-e2e-001" \
  -d '{
    "query": "What is the company'\''s policy for working from home?",
    "top_k": 5
  }' | uv run python -m json.tool

Or, even simpler, since jq is commonly available on macOS:

curl -s \
  -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: m10-4-e2e-001" \
  -d '{
    "query": "What is the company'\''s policy for working from home?",
    "top_k": 5
  }' | jq
First, though

Since Uvicorn is running, test:

curl http://127.0.0.1:8000/health

Expected:

{"status":"ok"}