import requests

# Ensure this URL matches exactly to how you've deployed and configured your FastAPI app on Hugging Face Spaces.
url = 'https://huggingface.co/spaces/yatharthk2/portfoliollm/api/query/'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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'  # Ensure this token is valid and has necessary permissions
}
data = {
    "question": "what work have you done in computer vision?"
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)  # Check the status code
print(response.text)         # Print the response body
