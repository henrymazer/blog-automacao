def generate_educacao_alunos_paragraph(data_loader, formatter, state_code: str = 'AC') -> str:
    """Generate paragraph about demographic impact on education.
    
    Args:
        data_loader: DataLoader instance with age group data
        formatter: BrazilianFormatter for number formatting
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        str: Formatted paragraph about education system changes
    """
    # Get state name and age group data
    state_name = data_loader.STATE_NAMES.get(state_code)
    if not state_name:
        return None
        
    age_data = data_loader.get_age_group_data(state_name)
    if not age_data:
        return None
        
    return (
        f"Com a projeção de queda de {formatter.format_number(age_data['pop_0_4_2024'])} para "
        f"{formatter.format_number(age_data['pop_0_4_2070'])} crianças de 0-4 anos até 2070, "
        f"o sistema educacional deverá enfrentar uma redução progressiva no número de alunos, "
        f"permitindo maior investimento por estudante mas também exigindo readequação da rede escolar."
    )
