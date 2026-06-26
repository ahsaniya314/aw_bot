import ast
import sys

def main():
    try:
        with open('handlers/callback_handler.py', 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        print(f"Error reading: {e}")
        return

    try:
        tree = ast.parse(source)
    except Exception as e:
        print(f"Error parsing: {e}")
        return

    print("Parsed successfully!")
    print(f"Has ast.unparse: {hasattr(ast, 'unparse')}")

if __name__ == '__main__':
    main()
