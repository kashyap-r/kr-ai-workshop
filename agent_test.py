import os
import chromadb
from crewai import Agent, Task, Crew, Process, LLM

# 1. Point CrewAI to your local Ollama server running on your M5 Max chip
local_llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434"
)

# 2. Test Connection to your Dockerized ChromaDB instance
print("Connecting to local ChromaDB memory store inside Docker...")
try:
    chroma_client = chromadb.HttpClient(host='localhost', port=8000)
    # Create or get an evaluation workspace collection
    collection = chroma_client.get_or_create_collection(name="agent_memory_test")
    print("✅ Successfully connected to Dockerized ChromaDB!")
except Exception as e:
    print(f"❌ Failed to connect to ChromaDB: {e}")
    print("Proceeding with Ollama local orchestration fallback...")

print("\nInitializing Team Agents...")

# 3. Define the AI Researcher Agent
researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover groundbreaking developments in AI architectures.',
    backstory="""You are a veteran technology scout. You excel at breaking 
    down complex technological advancements into easy-to-understand summaries.""",
    verbose=True,
    llm=local_llm
)

# 4. Define the AI Writer Agent
writer = Agent(
    role='Technical Content Writer',
    goal='Draft a compelling, beginner-friendly report based on research.',
    backstory="""You are an expert copywriter. You transform dense, highly technical 
    bullet points into polished, engaging blog posts.""",
    verbose=True,
    llm=local_llm
)

# 5. Define Tasks for the Agents
task_research = Task(
    description='Analyze the primary benefits of learning Agentic AI in 2026.',
    expected_output='A bulleted list highlighting 3 major advancements in multi-agent orchestration.',
    agent=researcher
)

task_write = Task(
    description='Take the research notes and write a short 2-paragraph educational blog post.',
    expected_output='A clean, publication-ready markdown blog post without generic fluff.',
    agent=writer
)

# 6. Group the agents together into a unified Crew
ai_crew = Crew(
    agents=[researcher, writer],
    tasks=[task_research, task_write],
    process=Process.sequential  # Task 1 feeds its output into Task 2 automatically
)

# 7. Kickoff the automated multi-agent workflow
print("\n🚀 Starting Multi-Agent Crew Execution on your M5 Max GPU...\n")
result = ai_crew.kickoff()

print("\n================== FINAL AGENT OUTPUT ==================\n")
print(result)
