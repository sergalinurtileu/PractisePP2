import pygame

def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()
    target_color = surface.get_at((x, y))
    if target_color == new_color: return
    
    pixels_to_fill = [(x, y)]
    while pixels_to_fill:
        curr_x, curr_y = pixels_to_fill.pop()
        if surface.get_at((curr_x, curr_y)) != target_color:
            continue
        surface.set_at((curr_x, curr_y), new_color)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr_x + dx, curr_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                pixels_to_fill.append((nx, ny))