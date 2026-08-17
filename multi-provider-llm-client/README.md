
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


Aug 18, 2026 - Add Helper and Logger Functions
