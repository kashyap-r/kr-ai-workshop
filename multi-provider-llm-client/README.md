
This mini-project is all about being able to connect to LLMs through APIs and converse with them i.e. provide a query / question and get a response.

The LLMs that are used here are .. 
    - Llama 
    - Gemini 
    - Grok 

To-Do: Observe the performance, usage, costs, errors, challenges in completing the task and log them here. 
This could potentially be used for Obervability and Evaluation later.

Aug 17, 2026 - Talk to LLMs 
1. Create API Keys, connect and converse with the below LLMs 
2. We'll now make the abstraction deal with things we've already encountered:
    authentication
    model selection
    provider-specific request formats
    response normalization
    API errors
    rate limits
    retries
    configuration

    Created pyproject.toml: as part of packaging/build/dependency management architecure of my project. 
    Why? 
    This was in response to the below error 
      File "/Users/kashyaprajpurohit/myGitHubRepos/kr-ai-workshop/multi-provider-llm-client/examples/test_clients.py", line 6, in <module>
        from llm_client.ollama_client import OllamaClient
        ModuleNotFoundError: No module named 'llm_client'

    Easy approach: Easiest way would have been to hack using the sys.path
    
    But used the TOML approach to make it a proper reusable, installable package so that we can install the project as a package, and not worry about the dependencies, paths, etc
    Tom's Obvious, minimal Language - TOML is a configuration/data serialization format designed to be easy for humans to read and write. 

    It is somewhat like the INI file.   


Aug 18, 2026 
1. Update Configuration
    - Model name is hardcoded
    - Credentials are mixed into application code 
    - Provider configuration isn't configurable 

    Solution: move configuration into .env 

2. Create a configuration module
    - create a new config.py containing the data class, gives us a structured configuration object 
                    LLMConfig
                    │
       ┌────────────┼────────────┐
    Provider      Models       Credentials
       │            │            │
    ollama       qwen3:8b       ...
    gemini       gemini...      ...
    groq         Qwen...        ...

    Note: # So later we'll add configuration validation and safe logging. Check config.py

3. Create LLMResponse 
    - to capture metadata thrown by the LLM response 
    - Data like 
        provider
        model
        latency
        input tokens
        output tokens
        total tokens    
    Why do we need it?
    The application gets the answer and the telemetry together and we need this information to establish benchmarks (Observability)
    Solution: Make changes on the base.py 

4. Latency - Each client should measure its own request duration 
    - refine ollama_client.py: Ollama's response may contain token/timing information, but we aren't assuming its exact structure yet. We'll inspect it separately and add that in the next iteration. 
    - refine gemini_client.py 
    - refine grok_client.py 
    - refine test_clients.py 


Future - Add Helper and Logger Functions
