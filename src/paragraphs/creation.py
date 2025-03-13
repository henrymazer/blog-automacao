from src.data.loader import get_first_census_data
from src.utils.api import get_state_creation_date
from src.utils.formatting import format_number

def generate_creation_paragraph(df, state_code='AC'):
    """Generate the third paragraph about state creation date and initial population."""
    # Get first census data
    census_data = get_first_census_data(df, state_code)
    if not census_data:
        return None
        
    primeiro_ano = census_data['ano']
    primeiro_valor = census_data['valor']
    
    # Get state creation date
    creation_year = get_state_creation_date()
    if not creation_year:
        return None
        
    creation_year = int(creation_year)
    primeiro_ano_int = int(primeiro_ano)
    
    if creation_year > primeiro_ano_int:
        return f"O estado foi criado em {creation_year}, mas o IBGE estimou a população para {primeiro_ano} em {format_number(int(primeiro_valor))} habitantes."
    else:
        return f"O estado foi criado em {creation_year}, e no Censo de {primeiro_ano} a população era de {format_number(int(primeiro_valor))} habitantes."
