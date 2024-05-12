import requests

response = requests.post(url="http://127.0.0.1:5000/airesponse",data='What are the field where we use Genai?')
print(response.json())