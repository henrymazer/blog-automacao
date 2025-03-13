import locale

# Set locale for number formatting
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def format_number(num):
    """Format a number according to Brazilian standards."""
    try:
        return locale.format_string("%d", num, grouping=True)
    except:
        return format(num, ",").replace(",", ".")

def format_historical_info(content):
    """Format historical information and handle source citations."""
    if not content:
        return None
    
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    formatted = []
    
    for p in paragraphs:
        p = ' '.join(p.split())  # Remove extra spaces
        p = p.replace('[1][3]', ' [Fonte: História do Acre](https://www.historia.acre.gov.br)')
        p = p.replace('[[', '[')
        p = p.replace('o[', 'o [')
        formatted.append(p)
    
    return '\n\n'.join(formatted)
