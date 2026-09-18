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