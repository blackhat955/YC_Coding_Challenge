#!/bin/bash

server_url="http://localhost:8080"

echo "=== Testing Python Code Execution API ==="
echo

echo "Test 1: Simple function returning JSON"
curl -X POST "$server_url/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "script": "def main():\n    return {\"message\": \"Hello World\", \"number\": 42}"
  }' | python3 -m json.tool
echo -e "\n"

echo "Test 2: Function with stdout output"
curl -X POST "$server_url/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "script": "def main():\n    print(\"Processing data...\")\n    return \"Task completed\""
  }' | python3 -m json.tool
echo -e "\n"

echo "Test 3: Using pandas"
curl -X POST "$server_url/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "script": "import pandas as pd\ndef main():\n    df = pd.DataFrame({\"name\": [\"Alice\", \"Bob\"], \"age\": [25, 30]})\n    print(f\"Created DataFrame with {len(df)} rows\")\n    return df.to_dict(\"records\")"
  }' | python3 -m json.tool
echo -e "\n"

echo "Test 4: Error case (division by zero)"
curl -X POST "$server_url/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "script": "def main():\n    return 1 / 0"
  }' | python3 -m json.tool
echo -e "\n"

echo "Test 5: Health check"
curl -X GET "$server_url/health" | python3 -m json.tool
echo -e "\n"

echo "=== All tests completed ==="