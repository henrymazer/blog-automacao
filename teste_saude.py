import os
from dotenv import load_dotenv
from src.utils.api import PerplexityAPI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

def test_health_request():
    """Test the improved health system request for Acre."""
    # Initialize API client
    api_client = PerplexityAPI(API_KEY)
    
    # Make request
    state_name = "Acre"
    response = api_client.get_health_system_news(state_name)
    
    # Print structured response
    print("\n--- RESULTADO DO TESTE ---")
    print("-" * 80)
    
    if response:
        if "positive" in response:
            print("ASPECTOS POSITIVOS:")
            print(response["positive"])
            print("-" * 40)
        
        if "challenges" in response:
            print("DESAFIOS ATUAIS:")
            print(response["challenges"])
            print("-" * 40)
            
        if "raw_content" in response:
            print("CONTEÚDO ORIGINAL (se não foi possível processar corretamente):")
            print(response["raw_content"])
    else:
        print("A requisição falhou. Verifique a chave de API e a conexão.")
    
    print("-" * 80)

if __name__ == "__main__":
    test_health_request()
