#!/usr/bin/env python3

import requests
import json

server_endpoint = "http://localhost:8080"

def run_script_test(python_code, test_description):
    print(f"\n=== {test_description} ===")
    print(f"Script:\n{python_code}")
    
    try:
        api_response = requests.post(
            f"{server_endpoint}/execute",
            json={"script": python_code},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {api_response.status_code}")
        print(f"Response: {json.dumps(api_response.json(), indent=2)}")
        
    except Exception as request_error:
        print(f"Error: {request_error}")

def main():
    
    run_script_test(
        'def main():\n    return {"message": "Hello World", "number": 42}',
        "Simple JSON return"
    )
    
    run_script_test(
        'def main():\n    print("Processing data...")\n    print("Almost done...")\n    return "Task completed"',
        "Function with stdout"
    )
    
    run_script_test(
        '''import pandas as pd
def main():
    df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})
    print(f"Created DataFrame with {len(df)} rows")
    return df.to_dict("records")''',
        "Using pandas"
    )
    
    run_script_test(
        '''import numpy as np
def main():
    arr = np.array([1, 2, 3, 4, 5])
    result = np.mean(arr)
    print(f"Array: {arr}")
    return {"mean": float(result), "sum": int(np.sum(arr))}''',
        "Using numpy"
    )
    
    run_script_test(
        'print("This script has no main function")',
        "No main function (should return None)"
    )
    
    run_script_test(
        'def main():\n    return "missing quote',
        "Syntax error case"
    )
    
    run_script_test(
        'def main():\n    return 1 / 0',
        "Runtime error case"
    )
    
    print("\n=== Health Check ===")
    try:
        health_response = requests.get(f"{server_endpoint}/health")
        print(f"Status Code: {health_response.status_code}")
        print(f"Response: {json.dumps(health_response.json(), indent=2)}")
    except Exception as health_error:
        print(f"Error: {health_error}")

if __name__ == "__main__":
    main()