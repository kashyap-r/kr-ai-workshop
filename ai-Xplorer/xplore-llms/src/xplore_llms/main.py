# xplore-llms/main.py
from common_lib import get_ai_response

def run_demo():
    result = get_ai_response("Hello from the sub-project POC!")
    print(result)

if __name__ == "__main__":
    run_demo()
