install = pip install -r requirements.txt
run = python main.py
clean = rm -rf .....
lint = flake8 . && mypy . --warn-return-any
--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint--strict = flake8 . && mypy --strict .