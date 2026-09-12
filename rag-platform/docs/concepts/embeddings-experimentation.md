Embeddings
    The evaluation of the embedding functionality will follow the below 
    steps. 

this experiment should answer one question"
    Which local, open-source embedding model gives us the best trade-off between retrieval 
    quality and operational cost for our RAG corpus?

1. Candidate A - all-MiniLM-L6-V2
name: sentence-transformers/all-MiniLM-L6-v2

1. Cndidate B - BAAI/bge-small-en-v1.5
ame: BAAI/bge-base-en-v1.5
3. Candidate C - BAAI/bge-base-en-v1.5
name: BAAI/bge-base-en-v1.5


Evaluation Parameter: 
    Does embedding the query allow us to retrieve the correct DocumentChunk?

Experimental Query Set: 
1. Query:
"How many days of annual leave are employees entitled to?"

Expected relevant:
Leave Policy chunk

2. Query:
"Can employees work from home?"

Expected relevant:
WFH Policy chunk

3. Query:
"What happens during a performance improvement plan?"

Expected relevant:
PIP / HR chunk

### Now add the dependencies 
cd python 

uv add --dev sentence-transformers 

After installation, verify the ebvironment

uv run python -c "from sentence_transformers import SentenceTransformer; print('sentence-transformers OK')"



