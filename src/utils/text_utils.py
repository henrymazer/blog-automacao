from typing import Optional

def numero_para_extenso(num: int) -> str:
    """Convert a number to its written form in Portuguese.
    
    Args:
        num: Number to convert (1-5)
        
    Returns:
        Number written in Portuguese
    """
    extenso = {
        1: "primeiro",
        2: "segundo",
        3: "terceiro",
        4: "quarto",
        5: "quinto"
    }
    return extenso.get(num, str(num))

def posicao_inversa(pos: int, total: int) -> str:
    """Get position from end in Portuguese (último, penúltimo, antepenúltimo).
    
    Args:
        pos: Current position
        total: Total number of items
        
    Returns:
        Position description in Portuguese
    """
    if pos == total:
        return "último"
    elif pos == total - 1:
        return "penúltimo"
    elif pos == total - 2:
        return "antepenúltimo"
    return str(pos)

def format_historical_info(content: Optional[str]) -> Optional[str]:
    """Format historical information with proper spacing and citations.
    
    Args:
        content: Raw historical information text
        
    Returns:
        Formatted text with proper spacing and citations
    """
    if not content:
        return None
    
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    formatted = []
    
    for p in paragraphs:
        # Remove extra spaces
        p = ' '.join(p.split())
        
        # Format citations
        p = p.replace('[1][3]', ' [Fonte: História do Acre](https://www.historia.acre.gov.br)')
        p = p.replace('[[', '[')
        p = p.replace('o[', 'o [')
        
        formatted.append(p)
    
    return '\n\n'.join(formatted)

def get_ranking_description(position: int, total: int, regional_position: Optional[int] = None, region: Optional[str] = None) -> str:
    """Generate ranking description in Portuguese based on position.
    
    Args:
        position: National ranking position
        total: Total number of states
        regional_position: Optional position within region
        region: Optional region name
        
    Returns:
        Formatted ranking description
    """
    if position <= 5:
        # Top 5 national
        pos_texto = numero_para_extenso(position)
        return f"Foi o {pos_texto} que mais cresceu no Brasil nesse período, proporcionalmente."
    elif position >= total - 2:
        # Bottom 3 national
        pos_texto = posicao_inversa(position, total)
        return f"Foi o {pos_texto} estado em crescimento no Brasil nesse período, proporcionalmente."
    elif regional_position and region:
        # Regional position
        return f"Foi o {regional_position}º estado que mais cresceu na região {region} nesse período, proporcionalmente."
    else:
        return f"Foi o {position}º estado em crescimento no Brasil nesse período, proporcionalmente."

def get_creation_description(creation_year: int, first_census_year: str, first_census_value: float) -> str:
    """Generate state creation description in Portuguese.
    
    Args:
        creation_year: Year state was created
        first_census_year: Year of first census data
        first_census_value: Population value from first census
        
    Returns:
        Formatted description of state creation and first census
    """
    creation_year = int(creation_year)
    first_census_year_int = int(first_census_year)
    
    if creation_year > first_census_year_int:
        return (f"O estado foi criado em {creation_year}, mas o IBGE estimou a população "
                f"para {first_census_year} em {first_census_value} habitantes.")
    else:
        return (f"O estado foi criado em {creation_year}, e no Censo de {first_census_year} "
                f"a população era de {first_census_value} habitantes.")
