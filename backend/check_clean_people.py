import json
from pathlib import Path

CLEAN_FILE = Path(__file__).parent / "people_clean.json"


def load_clean_people():
    with CLEAN_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def check_duplicates(people):
    seen_employee_nos = set()
    seen_card_nos = set()

    for person in people:
        employee_no = person["employee_no"].upper()
        card_no = person["card_no"].upper()

        if employee_no in seen_employee_nos:
            print("仍然存在重复工号：", employee_no)
            return False

        if card_no in seen_card_nos:
            print("仍然存在重复卡号：", card_no)
            return False

        seen_employee_nos.add(employee_no)
        seen_card_nos.add(card_no)

    return True


def main():
    people = load_clean_people()
    ok = check_duplicates(people)

    if ok:
        print("验证通过：people_clean.json 没有重复工号和重复卡号")
    else:
        print("验证失败：people_clean.json 仍有重复数据")


if __name__ == "__main__":
    main()