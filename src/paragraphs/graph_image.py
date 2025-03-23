def generate_graph_image_paragraph(data_loader, state_code: str = 'AC', graphs_dir: str = r"D:\jornalera-marista\censo-2022\dados\estados\graphs_pop_2024") -> str:
    """Generate markdown image reference for the state's population growth graph.
    
    Args:
        data_loader: DataLoader instance with census and growth data
        state_code: Two-letter state code (default: 'AC' for Acre)
        graphs_dir: Directory containing graph images (can be overridden)
        
    Returns:
        Markdown formatted image reference
    """
    # Get state info
    state_info, _, _, _ = data_loader.get_state_data(state_code)
    state_name = state_info['name']
    
    # Construct image path
    image_path = f"{graphs_dir}\\{state_name}.png"
    
    return f"![Gráfico de crescimento populacional do {state_name}]({image_path})"
