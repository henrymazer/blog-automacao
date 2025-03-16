from src.utils.text_utils import format_health_info

def generate_saude_atual_paragraph(data_loader, api_client, state_code: str = 'AC') -> str:
    """Generate paragraph about current health system status with recent news.
    
    Args:
        data_loader: DataLoader instance for state information
        api_client: PerplexityAPI instance for health news query
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        Formatted paragraph with health system news and analysis
    """
    # Get state name from code
    state_name = data_loader.STATE_NAMES.get(state_code)
    if not state_name:
        return None
        
    # Get current health system news and analysis
    health_news = api_client.get_health_system_news(state_name)
    if not health_news:
        return None
        
    # Clean text and sources
    text = health_news.replace("[1][3]", "")  # Remove stray source references
    
    # Split into sentences and format properly
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    formatted_sentences = []
    
    for sentence in sentences:
        # Clean up sentence formatting
        sentence = sentence.strip()
        if not sentence.endswith('.'):
            sentence += '.'
        formatted_sentences.append(sentence)
    
    # Join with double line breaks
    return "\n\n".join(formatted_sentences)
