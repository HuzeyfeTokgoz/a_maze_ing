# install = pip install -r requirements.txt
# run = python main.py
# clean = rm -rf .....
# lint = flake8 . && mypy . --warn-return-any
# --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
# lint--strict = flake8 . && mypy --strict .

run:
	python a_maze_ing_1.py config.txt

test: run
	./maze_analyzer.py maze.txt

.PHONY: run, test