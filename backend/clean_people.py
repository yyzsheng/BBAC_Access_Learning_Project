from pathlib import Path
import json

from person_json_safe import load_people

CLEAN_FILE = Path(__file__).parent / "people_clean.json"


def clean_people(people):
    clean_list = []
    seen_employee_nos = set()
    seen_card_nos = set()

    for person in people:
        employee_no = person["employee_no"].upper()
        card_no = person["card_no"].upper()

        if employee_no in seen_employee_nos:
            print("跳过重复工号：", employee_no, person["name"])
            continue

        if card_no in seen_card_nos:
            print("跳过重复卡号：", card_no, person["name"])
            continue

        person["employee_no"] = employee_no
        person["card_no"] = card_no

        clean_list.append(person)
        seen_employee_nos.add(employee_no)
        seen_card_nos.add(card_no)

    return clean_list


def save_clean_people(people):
    with CLEAN_FILE.open("w", encoding="utf-8") as file:
        json.dump(people, file, ensure_ascii=False, indent=4)


def main():
    people = load_people()
    clean_list = clean_people(people)
    save_clean_people(clean_list)
    print("清理完成，干净数据已保存到 people_clean.json")


if __name__ == "__main__":
    main()