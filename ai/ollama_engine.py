import requests

def ask_ollama(question):

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": question,
                "stream": False
            }
        )

        data = response.json()

        return data.get("response")

    except Exception as e:

        print("Ollama Error:", e)

        return None
        