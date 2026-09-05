

                    RAG PLATFORM
                         │
             ┌───────────┴───────────┐
             │                       │
          Python                 TypeScript
             │                       │
     AI/RAG internals          Application layer
             │                       │
      ┌──────┼──────┐          ┌─────┼─────┐
      │      │      │          │     │     │
   Parsing Embed Retrieval    API Streaming Auth
      │      │      │          │     │     │
      └──────┴──────┘          └─────┴─────┘
             │                       │
             └───────────┬───────────┘
                         │
                    Shared contracts
                    & architecture
                    