def generate_elderly_graph_image_paragraph(data_loader, state_code: str = 'AC') -> str:
    """Generate paragraph with elderly population graph image.
    
    Args:
        data_loader: DataLoader instance
        state_code: Two-letter state code
        
    Returns:
        Markdown formatted image link
    """
    state_info, _, _, _ = data_loader.get_state_data(state_code)
    state_name = state_info['name']
    
    graph_path = fr"D:\jornalera-marista\censo-2022\dados\estados\populacao_graficos_acima_65\estado_{state_name}_acima_65.png"
    
    return f"![Gráfico da população acima de 65 anos do {state_name}]({graph_path})"
