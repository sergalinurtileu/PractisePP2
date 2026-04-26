import pygame

def flood_fill(surface, x, y, new_color):
    """
    Fills a connected area of the same color with a new_color.
    This is an iterative implementation (using a stack) to avoid recursion limits.
    """
    # Get dimensions of the surface to stay within bounds
    width, height = surface.get_size()
    
    # Get the color of the pixel where we start (the color we want to replace)
    target_color = surface.get_at((x, y))
    
    # If the target color is already the new color, no need to do anything
    if target_color == new_color:
        return
    
    # Initialize the stack with the starting point
    pixels_to_fill = [(x, y)]
    
    while pixels_to_fill:
        # Get the next pixel coordinates from the stack
        curr_x, curr_y = pixels_to_fill.pop()
        
        # Check if the current pixel's color matches the color we are replacing
        if surface.get_at((curr_x, curr_y)) != target_color:
            continue
            
        # Change the current pixel's color to the new color
        surface.set_at((curr_x, curr_y), new_color)
        
        # Check all 4 adjacent directions (Up, Down, Right, Left)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr_x + dx, curr_y + dy
            
            # Ensure the neighbor is within the surface boundaries
            if 0 <= nx < width and 0 <= ny < height:
                pixels_to_fill.append((nx, ny))