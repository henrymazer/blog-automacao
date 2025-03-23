from src.utils.text_utils import format_health_info

def generate_saude_atual_paragraph(data_loader, api_client, state_code: str = 'AC') -> str:
    """Generate paragraphs about current health system status with clear separation between
    positive aspects and challenges.
    
    Args:
        data_loader: DataLoader instance for state information
        api_client: PerplexityAPI instance for health news query
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        Formatted paragraphs with health system analysis
    """
    # Get state name from code
    state_name = data_loader.STATE_NAMES.get(state_code)
    if not state_name:
        return None
        
    # Get current health system information with positive aspects and challenges
    health_info = api_client.get_health_system_news(state_name)
    if not health_info:
        return None
    
    # Format paragraphs
    paragraphs = []
    
    if "positive" in health_info:
        positive_text = health_info["positive"].strip()
        paragraphs.append(positive_text)
        
    if "challenges" in health_info:
        challenges_text = health_info["challenges"].strip()
        paragraphs.append(challenges_text)
    
    # If we have the raw content but couldn't parse it properly
    if "raw_content" in health_info and len(paragraphs) == 0:
        raw_text = health_info["raw_content"].strip()
        # Basic cleanup for raw content
        raw_text = raw_text.replace('\n\n', ' ')
        raw_text = ' '.join(raw_text.split())
        paragraphs.append(raw_text)
    
    # Join with double line breaks
    return "\n\n".join(paragraphs)
