import requests

def get_state_creation_date():
    """Get the creation date of Acre state from Perplexity AI."""
    api_key = "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"
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": "When was the state of Acre created in Brazil? Return only the year."
            }
        ],
        "max_tokens": 123,
        "temperature": 0.2,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error getting state creation date: {e}")
        return None

def get_historical_info(year):
    """Get historical information for a specific year from Perplexity AI."""
    api_key = "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"
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "Write a brief, concise response in Portuguese with exactly two short sentences. Write each sentence on a single line, followed by its source link. Keep sentences short and simple."
            },
            {
                "role": "user",
                "content": f"What was the main economic activity and political organization of Acre, Brazil in {year}? Write two short sentences in Portuguese, first about economic activity, second about political organization. Start each with 'Em {year}'. After each sentence, add a source like '[História do Acre](https://www.historia.acre.gov.br)'. Keep sentences brief."
            }
        ],
        "max_tokens": 500,
        "temperature": 0.2,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        # Clean up response and ensure proper formatting
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        return '\n\n'.join(paragraphs)
    except Exception as e:
        print(f"Error getting historical information: {e}")
        return None
