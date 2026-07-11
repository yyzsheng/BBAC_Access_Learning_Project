import json
from pathlib import Path
from person_functions import add_person, show_people
DATA_FILE = Path(__file__).parent / "people.json"
def save_people(person_list):
    """将人员列表保存到 JSON 文件中。"""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(person_list, 
                  file, 
                  ensure_ascii=False, 
                  indent=4)
    print(f"人员列表已保存到 {DATA_FILE}")


def load_people():
    """从 JSON 文件中加载人员列表。"""
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as file:
            person_list = json.load(file)
        print(f"已从 {DATA_FILE} 加载人员列表")
        return person_list
    else:
        print(f"{DATA_FILE} 不存在，返回空列表")
        return []
    


def main():
    people = load_people()
    print("当前人员列表：")
    show_people(people)

    print("\n=== 新增人员 ===")
    created = add_person(people)
    if created:
        save_people(people)
        print("\n=== 新增后的人员列表 ===")
        show_people(people)

if __name__ == "__main__":
    main()