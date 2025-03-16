import os
from dotenv import load_dotenv
from src.utils.api import PerplexityAPI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

def test_health_request():
    """Test the health system request for Acre."""
    # Initialize API client
    api_client = PerplexityAPI(API_KEY)
    
    # Make request
    state_name = "Acre"
    response = api_client.get_health_system_news(state_name)
    
    # Print raw response
    print("\nResposta da API (sem formatação):")
    print("-" * 80)
    print(response)
    print("-" * 80)

if __name__ == "__main__":
    test_health_request()
