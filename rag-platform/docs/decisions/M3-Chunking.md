Chunking 

The chunking architecture for this prototype will be small 

Chunking

[1] Define baseline strategy
        ↓
[2] Implement Chunker against existing Chunker protocol
        ↓
[3] Produce DocumentChunk objects
        ↓
[4] Persist chunks locally as JSONL
        ↓
[5] Preserve provenance + offsets
        ↓
[6] Add chunking version
        ↓
[7] Document infrastructure alternatives / ADR
        ↓
[8] Smoke-test on ZCompanyLLC



So... the chunk metadata will inherit from the parser class 

Chunk
│
├── chunk_id
├── document_id
├── document_version
├── chunking_version
├── sequence_number
├── start_offset
├── end_offset
├── text
└── metadata
      ├── path
      ├── filename
      ├── country
      ├── document_type
      └── ...



1. First implementation: structure-aware recursive chunking
We'll build a chunker that:
1. Tries to preserve paragraphs.
2. Splits oversized paragraphs.
3. Uses a target chunk size.
4. Uses overlap.
5. Preserves character offsets.
6. Generates deterministic ChunkIDs using our existing identity function.
7. Carries document metadata forward.
8. Has an explicit chunking_version.

Why not token-based immediately?
Because we're trying to understand the engineering boundary first.

Character-based chunking gives us a simple, deterministic implementation with no tokenizer dependency.

Later we can compare:
Character-based
       vs
Token-based
       vs
Structure-aware
       vs
Semantic

Proposed configuration
Let's start with:
chunk_size = 1000
chunk_overlap = 150

These are engineering defaults, not universal optimal values.

What to test?
short document → one chunk
large document → multiple chunks

Overlap
chunk[n][-overlap:]
==
chunk[n+1][:overlap]

Determinism
Same document → same chunk IDs.

Versioning
Changing:RecursiveChunker.VERSION
changes chunk IDs.

Validation
These should fail:
chunk_size=0
chunk_size=-1
chunk_overlap=-1
chunk_overlap >= chunk_size

Empty document
"" → []

Offsets
Verify:
document.text[chunk.start_offset:chunk.end_offset]==chunk.text
That last test is particularly valuable.

### Limitations of the current design and what we can do next?

1. Arbitrary character boundaries can be problematic.
2. How chunk size affects retrieval and generation.
3. How chunk size, overlap and tokenization interact.
4. Whether character-based, token-based, structure-aware or semantic chunking is the right choice

#### 1. Arbitrary character boundaries can be problematic.

Suppose our chunk size is 100 characters and overlap is 20.

Chunk 1: 0–100

The company provides parental leave to eligible employees. Employees must submit their request through the HR portal at least thirty days before the planned leave.


Chunk 2: 80–180

least thirty days before the planned leave. The request must include the expected start date and supporting documentation where applicable.

The problem is that the algorithm doesn't understand language.
It doesn't know:
- Where a sentence ends.
- Whether a paragraph contains one complete policy rule.
- Whether a heading belongs with the paragraph following it.
- Whether a list item depends on the introductory sentence.
- Whether a table row is meaningful without its column headings.

It simply counts characters.

The impact:
The user queries might produce incomplete retrieval. 

This can cause:
1. Lower retrieval quality because relevant evidence is fragmented.
2. Incomplete context passed to the LLM.
3. Answers that omit important conditions.
4. Citations pointing to incomplete evidence.
5. Greater dependence on overlap to recover lost context.

The fundamental issue is not that character-based chunking is inherently bad. It is that arbitrary boundaries can destroy semantic and structural relationships.

#### 2. Chunk size and its impact
Chunk size determines how much source content is grouped into one retrieval unit.
It is one of the most consequential RAG design decisions.
Consider three hypothetical configurations:

Small chunks (150–250 tokens)
Higher granularity
- More precise retrieval.
- Individual facts can be isolated.
- Greater risk of losing surrounding context.
- More chunks and potentially more index entries.
  
  Medium chunks (400–700 tokens)
  Balanced starting point
- Usually enough context for a policy paragraph or small section.
- Reasonable retrieval granularity.
- Manageable context assembly.
- A useful starting range for our HR corpus.
  
  Large chunks(900–1,500 tokens)
  More context, less precision
- Better chance of retaining complete sections.
- More unrelated material can accompany a relevant match.
- Retrieval can become less precise.
- More tokens consumed downstream.

These are illustrative ranges, not universal thresholds. The right size depends on the document structure, embedding model, retrieval method, query type and generation context budget.

What happens when chunk size changes?
Dimension	                Smaller chunks	        Larger chunks
Retrieval precision	        Often improves	        Can decline
Context completeness	        Can decline	        Often improves
Number of vectors	        Increases	        Decreases
Index storage	                Increases	        Decreases
Embedding workload	        Increases	        Decreases
Context assembly	        More fragments	        Fewer, larger fragments
Citation granularity	        Finer	                Coarser
Risk of unrelated content	Lower per chunk	        Higher per chunk

Retrieval precision and answer quality are not the same thing.
A small chunk might retrieve the exact sentence answering a question. But if the eligibility condition is in the preceding paragraph, the generator may not have enough information to answer correctly.

Conversely, a large chunk may contain all the information but also include several unrelated policies.

The objective is not to maximize chunk size or minimize it. It is to maximize the usefulness of the evidence retrieved.

Note: 
Understand the nature of information or response that needs to be served to the user query. That is also a good indicator of chun size. 

Begin with a target of 500 tokens per chunk, with a maximum around 700 tokens, and test a smaller and larger configuration later.

This is a starting hypothesis, not a final benchmark result.

#### Chunk size vs overlap vs tokenization
These three are related, but they solve different problems.
A. Chunk size
How much content should a chunk contain?
Target: 500 tokens
Maximum: 700 tokens

B. Overlap
How much content should consecutive chunks share?

For example:
Chunk 1: tokens 0–500
Chunk 2: tokens 450–950
Chunk 3: tokens 900–1400

Here, the overlap is 50 tokens.

Overlap helps preserve continuity when a logical unit is split between adjacent chunks.
But overlap is not free.

For a 500-token chunk with 50-token overlap, the effective new content per chunk is 450 tokens.

That means approximately 11% more chunk content is processed than with non-overlapping chunks, ignoring document boundaries and structural adjustments.

Excessive overlap can result in:
- More vectors and storage.
- Duplicate retrieval results.
- Repeated evidence in the prompt.
- More embedding computation.
- Less diversity in the retrieved context.

Overlap should be used to address boundary discontinuity, not as a substitute for good boundary selection.

For our first structure-aware implementation, I'd start with 10% overlap as a maximum target, but allow zero overlap when complete structural units fit naturally.

C. Tokenization
This is where things get interesting.

A character is not a token.

Consider: parental leave
This might be represented as:
- 14 characters, including the space.
- Two words.
- One or more model tokens, depending on the tokenizer.
Now consider:
internationalisation

A tokenizer may split this into multiple tokens.

And consider multilingual content, special characters, identifiers and code. Character counts become even less reliable as a proxy for model input size.

Why does this matter?

Your embedding model has an input token limit. Your generation model has a context window. Both operate on tokens, not arbitrary character counts.

If your chunking is based solely on characters, you cannot reliably guarantee that every chunk fits within the model's token budget.

Character count vs token count
Property	        Character-based	                Token-based
Unit	                Characters	                Model tokens
Implementation	        Simple	                        Requires tokenizer
Model input limits	Approximate	                Much more reliable
Language sensitivity	High	                        Depends on tokenizer
Reproducibility	        Independent of tokenizer	Tied to tokenizer/version
Processing overhead	Low	                        Additional tokenization

The important distinction
Token-based chunking doesn't automatically create semantically good chunks.

It only controls the size more accurately.

You could still split a heading from its paragraph, or a condition from its exception, even if every chunk contains exactly 500 tokens.

This leads to the central design decision:
Use document structure to decide where to split; use tokenization to decide how much content can fit.

#### 4. Comparing the four chunking strategies
Let's examine each strategy independently.

4.1 Character-based chunking

How it works
Split text after a fixed number of characters, optionally with overlap.

Text
  ↓
Fixed character windows
  ↓
Chunks

Advantages
- Very simple.
- Fast and deterministic.
- No tokenizer dependency.
- Easy to test and debug.

Disadvantages
- Can split sentences and paragraphs.
- Does not understand headings, lists or tables.
- Character count is a poor proxy for token count.
- Can fragment important policy statements.
Best suited for: Baselines, simple unstructured text, initial prototypes.

Our assessment: Good as a baseline, not sufficient as the final strategy for this project.

4.2 Token-based chunking
How it works
Tokenize the text and split it into fixed token windows.

Text
  ↓
Tokenizer
  ↓
Token sequence
  ↓
Fixed token windows
  ↓
Chunks

Advantages
- Better control over embedding input limits.
- Predictable token budgets.
- More reliable context-window management.
- Useful for comparing models with different tokenizers.

Disadvantages
- Requires tokenizer integration.
- Can split sentences and semantic units.
- Different models may use different tokenizers.
- Tokenizer version changes can affect chunk boundaries.
Best suited for: Systems where model input limits and context budgets are important.

Our assessment: Essential as a size constraint, but insufficient as the only chunking strategy.

4.3 Structure-aware chunking
How it works

Identify document structures and preserve meaningful boundaries.

For example:
# Parental Leave Policy

## Eligibility

Employees who have completed...

## Entitlement

Eligible employees receive...

## Application Process

Employees must submit...

The chunker understands that these sections are meaningful units.

It attempts to keep:
- Headings with their content.
- Paragraphs intact.
- Lists together.
- Table headers with their rows.
- Related policy statements together.
If a section exceeds the maximum token budget, it splits that section further using smaller structural units.

Advantages
- Preserves document meaning and hierarchy.
- More useful retrieval units.
- Better evidence completeness.
- Natural fit for policy documents, handbooks and technical documentation.
Disadvantages
- Requires format-specific parsing or structural extraction.
- Different document formats have different structures.
- Large sections still require splitting.
- Tables and complex PDFs need additional handling.

Best suited for: Enterprise knowledge bases, policy documents, technical documentation, handbooks and structured content.

Our assessment: This should be our primary strategy.

4.4 Semantic chunking

How it works

The chunker attempts to identify changes in meaning or topic.

For example:
Sentence 1: Sweden parental leave entitlement.
Sentence 2: Sweden eligibility requirements.
Sentence 3: Sweden application procedure.

           TOPIC SHIFT

Sentence 4: Germany parental leave entitlement.
Sentence 5: Germany eligibility requirements.


A semantic chunker may use sentence embeddings and similarity comparisons to detect topic shifts.

A simplified flow:
Document
   ↓
Sentence segmentation
   ↓
Sentence embeddings
   ↓
Similarity analysis
   ↓
Topic boundary detection
   ↓
Semantic chunks


Advantages
- Can identify topic transitions.
- Can group related sentences.
- Useful when document structure is poor or inconsistent.
- Potentially useful for unstructured content.

Disadvantages
- More computationally expensive.
- Requires embedding calculations during chunking.
- Similarity thresholds require tuning.
- Can produce inconsistent chunk sizes.
- Semantic similarity does not guarantee logical completeness.
A particularly important limitation: two sentences can be semantically similar but logically belong to different policy conditions. Conversely, an exception may be semantically dissimilar but must remain with the rule it qualifies.

Best suited for: Large, unstructured or poorly formatted content where structural boundaries are unavailable or insufficient.

Our assessment: Valuable as an advanced option, but not our default.

#### 6. Which one should we choose?
Recommended architecture
Structure-aware, token-bounded, with controlled overlap.

I would not choose only one of the four as an isolated technique.

Recommended chunking pipeline
                Parsed document
                PDF / Markdown / TXT
                        ↓
                Structure detection
                Headings, paragraphs, lists, tables
                        ↓
                Structural grouping
                Preserve related content and heading hierarchy
                        ↓
                Token budget enforcement
                Target 500 tokens · maximum 700 tokens
                        ↓
                Controlled overlap
                Start around 10%, avoid unnecessary duplication
                        ↓
                DocumentChunk[]
                Stable IDs · offsets · metadata · lineage

How should it behave?
1. Try to keep a complete section or paragraph together.
2. If the structural unit exceeds the token limit, split it at sentence boundaries.
3. If a sentence is itself too large, split it at a sensible whitespace boundary.
4. Never exceed the configured maximum token budget, except where a documented special-case policy explicitly permits it.
5. Retain heading hierarchy and source metadata.
6. Use overlap only when splitting creates a genuine continuity problem.
7. Record the chunking configuration and version so that the index can be rebuilt consistently.
Semantic chunking can be added later as an alternative strategy and benchmarked against the structure-aware baseline.



Question: 
Whee is the source metadata stored ?

#### Evaluating Chunking Strategy 

7. How we should evaluate the decision
This is where your Golden Dataset becomes important.

We shouldn't declare structure-aware chunking the winner simply because it sounds better.

We need to compare the strategies experimentally.

For the same corpus, build alternative chunk sets:
Experiment	Strategy	Target size	Overlap
C1	Character-based	2,000 characters	200 characters
C2	Token-based	500 tokens	50 tokens
C3	Structure-aware + token limit	500 tokens	Up to 50 tokens
C4	Semantic + token limit	500 tokens	Controlled

These are initial experiment configurations, not fixed requirements.

Then measure:

Chunk quality
- Structural completeness.
- Sentence/paragraph fragmentation.
- Chunk size distribution.
- Oversized chunk count.
- Duplicate content caused by overlap.
Retrieval quality
- Recall@K.
- Precision@K.
- MRR.
- Hit Rate@K.
Downstream answer quality
- Correctness.
- Groundedness.
- Citation accuracy.
- Completeness of answer.
Operational cost
- Chunk generation time.
- Number of chunks.
- Embedding token volume.
- Index size.
- Query-time context size.

## Where to persist data (Chunks + embeddings + metadata) ?

JSONL ( for )

Relational DB (PostgreSQL)

Vector DB 
        A vector database can store embeddings together with chunk content and metadata, but whether chunk content should be co-located with vectors or retrieved from a separate content store is an architectural trade-off.

        The index is also maintained by the vector database, but there's an important distinction between the data you store and the index structure the database builds over that data.

                            Vector Database
                ┌─────────────────────────────────────────────────┐
                │                                                 │
                │  Stored records                                 │
                │  ┌───────────────────────────────────────────┐  │
                │  │ chunk_id                                  │  │
                │  │ vector                                    │  │
                │  │ chunk text                                │  │
                │  │ metadata                                  │  │
                │  └───────────────────────────────────────────┘  │
                │                                                 │
                │  Index                                         │
                │  ┌───────────────────────────────────────────┐  │
                │  │ HNSW / IVF / other ANN structure          │  │
                │  │                                           │  │
                │  │ enables fast vector similarity search     │  │
                │  └───────────────────────────────────────────┘  │
                │                                                 │
                └─────────────────────────────────────────────────┘

Search engine (Elasticsearch / OpenSearch)
        Features expected
                BM25
                +
                dense vectors
                +
                metadata filtering
                +
                hybrid retrieval


### The pipeline at this stage is 

Raw
 ↓
Parse
 ↓
Parsed artifacts
 ↓
Chunk
 ↓
Chunk artifacts
 ↓
Embed
 ↓
Vector + chunk + metadata
 ↓
Index
 ↓
Vector DB
 ↓
Retriever

