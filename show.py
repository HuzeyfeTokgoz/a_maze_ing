def print_maze(grid, entry, exit, solution="", pattern_cells=frozenset()):
    steps = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    path = {entry}
    x, y = entry
    for letter in solution:
        dx, dy = steps[letter]
        x, y = x + dx, y + dy
        path.add((x, y))

    height, width = len(grid), len(grid[0])
    print("+" + "".join("---+" if grid[0][x] & 1 else "   +"
                        for x in range(width)))
    for y in range(height):
        middle = "|" if grid[y][0] & 8 else " "
        bottom = "+"
        for x in range(width):
            if (x, y) in pattern_cells:
                middle += "###"
            elif (x, y) == entry:
                middle += " E "
            elif (x, y) == exit:
                middle += " X "
            elif (x, y) in path:
                middle += " * "
            else:
                middle += "   "

            if grid[y][x] & 2:
                middle += "|"
            elif (x, y) in path and (x + 1, y) in path:
                middle += "*"
            else:
                middle += " "

            if grid[y][x] & 4:
                bottom += "---+"
            elif (x, y) in path and (x, y + 1) in path:
                bottom += " * +"
            else:
                bottom += "   +"
        print(middle)
        print(bottom)