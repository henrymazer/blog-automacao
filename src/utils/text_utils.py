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
    
    # Split paragraphs and clean each one
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    formatted = []
    
    for p in paragraphs:
        # Remove extra spaces
        p = ' '.join(p.split())
        
        # Format citations to match exact format
        p = p.replace('[1][3]', ' [Fonte: História do Acre](https://www.historia.acre.gov.br)')
        p = p.replace('[[', '[')
        p = p.replace('o[', 'o [')
        p = p.replace('[Fonte:', ' [Fonte:')
        
        formatted.append(p)
    
    # Join with double line breaks
    return '\n\n'.join(formatted)

def format_health_info(content: Optional[str]) -> Optional[str]:
    """Format health system information with proper spacing and citations.
    
    Args:
        content: Raw health system information text
        
    Returns:
        Formatted text with proper spacing and citations
    """
    if not content:
        return None
    
    # Split content into text and sources
    parts = content.split('[1]')
    if len(parts) != 2:
        return content
    
    main_text = parts[0].strip()
    sources = '[1]' + parts[1].strip()
    
    # Clean up main text
    main_text = ' '.join(main_text.split())  # normalize spaces
    main_text = main_text.replace('..', '.')  # fix double periods
    
    # Split into sentences and clean
    sentences = []
    for s in main_text.split('.'):
        s = s.strip()
        if s:
            if not s.endswith('.'):
                s += '.'
            sentences.append(s)
    
    # Format sources
    sources = sources.replace(' [', '\n\n[')  # separate source list with line breaks
    sources = sources.replace('.html]', '.html)]')  # fix link formatting
    
    # Combine everything with proper spacing
    formatted_text = '\n\n'.join(sentences)
    formatted_text = formatted_text.rstrip('.')  # remove trailing period before sources
    
    return f"{formatted_text}\n\n{sources}"

def get_ranking_description(position: int, total: int) -> str:
    """Generate general ranking description in Portuguese.
    
    Args:
        position: National ranking position
        total: Total number of states
        
    Returns:
        Formatted ranking description for general growth
    """
    if position <= 5:
        pos_texto = numero_para_extenso(position)
        description = f"{pos_texto} lugar"
    elif position >= total - 2:
        pos_texto = posicao_inversa(position, total)
        description = f"{pos_texto} lugar"
    else:
        description = f"{position}ª posição"
    
    return f"este fato coloca o estado no {description} no ranking de crescimento populacional por estados do Brasil durante esse período, em termos percentuais"

def get_period_ranking_description(position: int) -> str:
    """Generate specific period ranking description in Portuguese.
    
    Args:
        position: Ranking position
        
    Returns:
        Formatted ranking description for specific period
    """
    pos_texto = numero_para_extenso(position) if position <= 5 else f"{position}º"
    return f"foi o {pos_texto} estado que mais cresceu no Brasil, em termos percentuais"

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
