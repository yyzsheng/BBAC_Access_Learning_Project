import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "people.json"


def load_people():
    if not DATA_FILE.exists():
        print("people.json 不存在，返回空列表")
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            people = json.load(file)
        return people
    except json.JSONDecodeError:
        print("错误：people.json 不是正确的 JSON 格式")
        return []


def save_people(people):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(people, file, ensure_ascii=False, indent=4)


def main():
    people = load_people()
    print(people)


if __name__ == "__main__":
    main()