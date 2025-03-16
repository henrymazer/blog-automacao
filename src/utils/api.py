from typing import Optional, Dict, Any
import requests
import json

class PerplexityAPI:
    def __init__(self, api_key: str):
        """Initialize the Perplexity API client.
        
        Args:
            api_key: Authentication key for Perplexity AI API
        """
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, messages: list, max_tokens: int = 500) -> Optional[Dict[str, Any]]:
        """Make a request to the Perplexity AI API.
        
        Args:
            messages: List of message objects for the conversation
            max_tokens: Maximum tokens in the response
            
        Returns:
            API response data or None if request fails
        """
        data = {
            "model": "sonar",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.2,
            "top_p": 0.9,
            "return_images": False,
            "return_related_questions": False,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 1
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API request failed: {e}")
            return None
    
    def get_state_creation_date(self) -> Optional[str]:
        """Get the creation date of Acre state.
        
        Returns:
            Year of state creation or None if request fails
        """
        messages = [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": "When was the state of Acre created in Brazil? Return only the year."
            }
        ]
        
        result = self._make_request(messages, max_tokens=123)
        if result and 'choices' in result:
            return result['choices'][0]['message']['content']
        return None
    
    def get_historical_info(self, year: str) -> Optional[str]:
        """Get historical information about Acre for a specific year.
        
        Args:
            year: Year to get historical information for
            
        Returns:
            Formatted historical information or None if request fails
        """
        messages = [
            {
                "role": "system",
                "content": "Write a brief, concise response in Portuguese with exactly two short sentences. Write each sentence on a single line, followed by its source link. Keep sentences short and simple."
            },
            {
                "role": "user",
                "content": (
                    f"What was the main economic activity and political organization of Acre, Brazil "
                    f"in {year}? Write two short sentences in Portuguese, first about economic "
                    f"activity, second about political organization. Start each with 'Em {year}'. "
                    f"After each sentence, add a source like '[História do Acre]"
                    f"(https://www.historia.acre.gov.br)'. Keep sentences brief."
                )
            }
        ]
        
        result = self._make_request(messages, max_tokens=500)
        if result and 'choices' in result:
            content = result['choices'][0]['message']['content']
            # Clean up response and ensure proper formatting
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            return '\n\n'.join(paragraphs)
        return None
