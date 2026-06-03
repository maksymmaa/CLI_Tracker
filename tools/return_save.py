import json, os

def tasks_save(filename) -> list | list[dict[str, str]]:
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f'Warning: could not read save file: {e}\n')
        return []