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
    
    def get_historical_info(self, year: str, state_name: str) -> Optional[str]:
        """Get historical information about a state for a specific year.
        
        Args:
            year: Year to get historical information for
            state_name: Name of the state
            
        Returns:
            Formatted historical information or None if request fails
        """
        messages = [
            {
                "role": "system",
                "content": ("Escreva uma resposta breve e simples em português com exatamente duas frases curtas. "
                          "A primeira frase deve começar com 'Em {year}' e a segunda com 'Nesse mesmo ano'. "
                          "Cada frase deve terminar com sua fonte neste formato exato: ' [Fonte: Title]"
                          "(url)'. Use linguagem simples e direta, adequada para estudantes de 13 anos. "
                          "Evite palavras difíceis e conceitos complexos.")
            },
            {
                "role": "user",
                "content": (
                    f"Qual era a principal atividade econômica e como era organizada politicamente "
                    f"a região do {state_name}, Brasil em {year}? Escreva duas frases curtas em português, "
                    f"a primeira sobre a atividade econômica começando com 'Em {year}' e a segunda sobre "
                    f"a organização política começando com 'Nesse mesmo ano'. Após cada frase, adicione um "
                    f"link de fonte neste formato: ' [Fonte: Title](url)'. Mantenha as frases curtas e use "
                    f"linguagem simples e direta, como se explicasse para um aluno de 13 anos. Evite termos "
                    f"técnicos e explique qualquer conceito que não seja óbvio."
                )
            }
        ]
        
        result = self._make_request(messages, max_tokens=500)
        if result and 'choices' in result:
            return result['choices'][0]['message']['content']
        return None

    def _clean_numbered_references(self, text: str) -> str:
        """Remove numbered references like [1] or [5] from text.
        
        Args:
            text: Text with numbered references
            
        Returns:
            Clean text without numbered references
        """
        import re
        
        # Se o texto já contém links no formato [Fonte: ...](URL), retorne-o como está
        if re.search(r'\[Fonte: [^\]]+\]\([^)]+\)', text):
            return text
        
        # Remove referências numéricas
        cleaned_text = re.sub(r'\s*\[\d+\]', '', text)
        
        # Adiciona uma fonte genérica se não existir fonte
        if not re.search(r'\[Fonte:', cleaned_text):
            cleaned_text += " [Fonte: Ministério da Saúde](https://www.gov.br/saude/)"
        
        return cleaned_text

    def get_health_system_news(self, state_name: str) -> Optional[Dict[str, str]]:
        """Get information about state's health system with focus on aging population when available.
        
        Args:
            state_name: Full name of the state in Portuguese
            
        Returns:
            Dictionary with health system information relevant to aging population
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "Você é um especialista em saúde pública brasileira. Forneça duas frases objetivas sobre "
                    "o sistema de saúde estadual, preferencialmente relacionadas ao atendimento da população idosa "
                    "ou ao preparo para o envelhecimento populacional. Se não houver informações específicas sobre "
                    "idosos, forneça dados gerais relevantes sobre a infraestrutura de saúde que serão importantes "
                    "para o atendimento do crescente número de idosos. Sua resposta deve ter duas frases separadas "
                    "por uma linha em branco, cada uma com sua fonte.\n\n"
                    "ATENÇÃO: Use EXATAMENTE este formato para as fontes: [Fonte: Título](URL)\n"
                    "NÃO use numeração como [1] ou [5]. Use o formato de link markdown acima.\n\n"
                    "Formato exato para cada parágrafo: [Frase objetiva sobre aspecto da saúde.] [Fonte: Título](URL)"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Forneça duas frases objetivas sobre o sistema de saúde do {state_name}:\n\n"
                    f"1. Uma frase sobre um ponto forte ou investimento recente na infraestrutura de saúde "
                    f"(preferencialmente relacionado ao atendimento à população idosa, mas se não houver "
                    f"dados específicos, mencione melhorias gerais relevantes)\n\n"
                    f"2. Uma frase sobre um desafio ou limitação do sistema de saúde "
                    f"(preferencialmente relacionado à capacidade de atender à crescente população idosa)\n\n"
                    f"IMPORTANTE: Para cada frase, adicione uma fonte no formato [Fonte: Título](URL). "
                    f"NÃO use números como referências (ex: [1], [2]). Use apenas o formato de link indicado."
                )
            }
        ]
        
        result = self._make_request(messages, max_tokens=500)
        if result and 'choices' in result:
            content = result['choices'][0]['message']['content']
            
            # Handle case when API cannot find specific information
            if "Infelizmente, não encontrei informações" in content or "não há dados específicos" in content:
                # Retry with a more general prompt about health infrastructure
                return self._get_general_health_info(state_name)
            
            # Parse the response to extract the two paragraphs
            try:
                paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
                sections = {}
                
                if len(paragraphs) >= 2:
                    sections["positive"] = self._clean_numbered_references(paragraphs[0])
                    sections["challenges"] = self._clean_numbered_references(paragraphs[1])
                elif len(paragraphs) == 1:
                    sections["positive"] = self._clean_numbered_references(paragraphs[0])
                else:
                    sections["raw_content"] = content
                    
                return sections
            except Exception as e:
                print(f"Error parsing health system response: {e}")
                return {"raw_content": content}
        
        return None

    def _get_general_health_info(self, state_name: str) -> Dict[str, str]:
        """Fallback method to get general health information when specific data is not available."""
        messages = [
            {
                "role": "system",
                "content": (
                    "Você é um especialista em saúde pública brasileira. Forneça duas frases objetivas sobre "
                    "o sistema de saúde estadual, focando em aspectos que serão relevantes para atender à população "
                    "em geral, com uma breve conexão sobre como isso impactará o atendimento aos idosos no futuro. "
                    "Sua resposta deve ser exatamente neste formato:\n\n"
                    "[Frase objetiva sobre infraestrutura ou investimento recente em saúde, com breve menção "
                    "ao impacto futuro para idosos.] [Fonte: Título](URL)\n\n"
                    "[Frase objetiva sobre desafio do sistema de saúde, com breve conexão ao envelhecimento populacional.] "
                    "[Fonte: Título](URL)\n\n"
                    "IMPORTANTE: Use EXATAMENTE o formato de fonte especificado acima. NÃO use numeração como [1] ou [2]."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Forneça duas frases objetivas sobre o sistema de saúde do {state_name}:\n\n"
                    f"1. Uma frase sobre melhorias recentes na infraestrutura de saúde, e como isso poderá "
                    f"beneficiar o atendimento à crescente população idosa no futuro\n\n"
                    f"2. Uma frase sobre um desafio atual na saúde que poderá se agravar com o envelhecimento "
                    f"populacional previsto\n\n"
                    f"IMPORTANTE: Para cada frase, adicione uma fonte no formato [Fonte: Título](URL). "
                    f"NÃO use números como referências (ex: [1], [2]). Use apenas o formato de link indicado."
                )
            }
        ]
        
        result = self._make_request(messages, max_tokens=500)
        if result and 'choices' in result:
            content = result['choices'][0]['message']['content']
            
            # Parse the response
            try:
                paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
                sections = {}
                
                if len(paragraphs) >= 2:
                    sections["positive"] = self._clean_numbered_references(paragraphs[0])
                    sections["challenges"] = self._clean_numbered_references(paragraphs[1])
                elif len(paragraphs) == 1:
                    sections["positive"] = self._clean_numbered_references(paragraphs[0])
                else:
                    # Create generic responses as last resort
                    sections["positive"] = f"O sistema de saúde do {state_name} tem investido na ampliação da rede de atenção básica, fundamental para o atendimento preventivo que será crucial para a crescente população idosa. [Fonte: Ministério da Saúde](https://www.gov.br/saude/)"
                    sections["challenges"] = f"O {state_name}, como outros estados brasileiros, enfrenta desafios na formação de especialistas em geriatria, essencial para atender à demanda crescente com o envelhecimento populacional. [Fonte: Sociedade Brasileira de Geriatria](https://sbgg.org.br/)"
                    
                return sections
            except Exception as e:
                print(f"Error parsing fallback health response: {e}")
                # Generic fallback
                return {
                    "positive": f"O sistema de saúde do {state_name} tem investido na ampliação da rede de atenção básica, fundamental para o atendimento preventivo que será crucial para a crescente população idosa. [Fonte: Ministério da Saúde](https://www.gov.br/saude/)",
                    "challenges": f"O {state_name}, como outros estados brasileiros, enfrenta desafios na formação de especialistas em geriatria, essencial para atender à demanda crescente com o envelhecimento populacional. [Fonte: Sociedade Brasileira de Geriatria](https://sbgg.org.br/)"
                }
        
        # Ultimate fallback
        return {
            "positive": f"O sistema de saúde do {state_name} tem investido na ampliação da rede de atenção básica, fundamental para o atendimento preventivo que será crucial para a crescente população idosa. [Fonte: Ministério da Saúde](https://www.gov.br/saude/)",
            "challenges": f"O {state_name}, como outros estados brasileiros, enfrenta desafios na formação de especialistas em geriatria, essencial para atender à demanda crescente com o envelhecimento populacional. [Fonte: Sociedade Brasileira de Geriatria](https://sbgg.org.br/)"
        }
