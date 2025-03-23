def generate_fertility_graph_image_paragraph(data_loader, state_code: str = 'AC') -> str:
    """Generate paragraph showing fertility graph image.
    
    Args:
        data_loader: DataLoader instance
        state_code: Two-letter state code
        
    Returns:
        Formatted paragraph with graph image markdown
    """
    state_info, _, _, _ = data_loader.get_state_data(state_code)
    state_name = state_info['name']
    
    image_path = (
        f"D:\\jornalera-marista\\censo-2022\\dados\\estados\\"
        f"populacao_graficos_0_4_anos\\estado_{state_name}.png"
    )
    
    return f"![Gráfico da população de 0 a 4 anos do {state_name}]({image_path})"
