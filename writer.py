def write_output(filename: str, grid: list[list[int]], entry: tuple[int, int],
                 exit: tuple[int, int], solution: str) -> None:

    with open(filename, "w", encoding="utf-8") as file:
        for row in grid:
            file.write("".join(format(cell, "x") for cell in row) + "\n")
        file.write("\n")
        file.write(f"{entry[0]},{entry[1]}\n")
        file.write(f"{exit[0]},{exit[1]}\n")
        file.write(solution + "\n")