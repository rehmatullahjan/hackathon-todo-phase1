import requests
import json

base_url = "http://localhost:8000"

def test_create(payload, name):
    try:
        response = requests.post(f"{base_url}/tasks", json=payload)
        print(f"Test '{name}': Status {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Test '{name}' Failed: {e}")

# Payload 1: Base case (Minimal)
payload1 = {
    "title": "Minimal Task"
}
test_create(payload1, "Minimal")

# Payload 2: With Priority (lowercase)
payload2 = {
    "title": "Priority Lower",
    "priority": "high"
}
test_create(payload2, "Priority Lower")

# Payload 3: With Priority (Capitalized) - Expected Fail
payload3 = {
    "title": "Priority Cap",
    "priority": "High"
}
test_create(payload3, "Priority Cap")

# Payload 4: Tags as JSON string
payload4 = {
    "title": "Tags JSON String",
    "tags": "[\"tag1\", \"tag2\"]"
}
test_create(payload4, "Tags JSON String")

# Payload 5: Tags as list (Should fail if model expects str)
payload5 = {
    "title": "Tags List",
    "tags": ["tag1", "tag2"]
}
test_create(payload5, "Tags List")

# Payload 6: Full Payload mimicking Frontend
payload6 = {
    "title": "Frontend Mimic",
    "description": "Desc",
    "status": "pending",
    "priority": "urgent",
    "category": "work",
    "tags": "[\"production\", \"v1\"]",
    "due_date": "2025-01-01",
    "start_date": "2025-01-01"
}
test_create(payload6, "Frontend Mimic w/ Date String")

# Payload 7: Dates as null
payload7 = {
    "title": "Dates Null",
    "due_date": None,
    "start_date": None
}
test_create(payload7, "Dates Null")

# Payload 8: Dates as empty string (Frontend might do this?)
payload8 = {
    "title": "Dates Empty String",
    "due_date": "",
    "start_date": ""
}
test_create(payload8, "Dates Empty String")
