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
                "content": ("Write a brief, concise response in Portuguese with exactly two short sentences. "
                          "Each sentence should end with its source in this exact format: ' [Fonte: Title]"
                          "(url)'. Start each sentence with 'Em {year}'. Keep sentences brief.")
            },
            {
                "role": "user",
                "content": (
                    f"What was the main economic activity and political organization of Acre, Brazil "
                    f"in {year}? Write two short sentences in Portuguese, first about economic "
                    f"activity, second about political organization. Start each with 'Em {year}'. "
                    f"After each sentence, add a source link in this format: ' [Fonte: Title]"
                    f"(url)'. Keep sentences brief."
                )
            }
        ]
        
        result = self._make_request(messages, max_tokens=500)
        if result and 'choices' in result:
            return result['choices'][0]['message']['content']
        return None

    def get_health_system_news(self, state_name: str) -> Optional[str]:
        """Get recent news about state's health system and analyze its future.
        
        Args:
            state_name: Full name of the state in Portuguese
            
        Returns:
            Formatted paragraph with news and analysis, or None if request fails
        """
        messages = [
            {
                "role": "system",
                "content": ("Write a concise response in Portuguese about the current health system "
                          "with exactly 3 complete sentences: recent achievements, specific improvements, "
                          "and current challenges/future concerns. Each sentence must end with "
                          "a period. Do not include source references in the sentences. After the "
                          "sentences, list sources separately, each on its own line.")
            },
            {
                "role": "user",
                "content": (
                    f"Escreva sobre a situação atual do sistema de saúde do {state_name}, "
                    f"em 4 frases: conquistas recentes, melhorias específicas, desafios atuais "
                    f"e preocupações futuras. Indique fontes com [1], [2], etc. e liste-as no final. "
                    f"Use dados recentes de 2022-2024."
                )
            }
        ]
        
        result = self._make_request(messages, max_tokens=500)
        if result and 'choices' in result:
            content = result['choices'][0]['message']['content']
            # Clean up formatting
            content = content.replace('\n', ' ').strip()
            return content
        return None
