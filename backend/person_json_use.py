from person_json_safe import load_people, save_people

def employee_no_exists(people, employee_no):
    for person in people:
        if person["employee_no"].upper() == employee_no.upper():
            return True
    return False

def card_no_exists(people, card_no):
    for person in people:
        if person["card_no"].upper() == card_no.upper():
            return True
    return False

def main():
    people = load_people()

    print("当前人员：")
    for person in people:
        print(person["name"], person["employee_no"], person["person_type"])

    name = input("请输入姓名：").strip()
    employee_no = input("请输入工号：").strip().upper()
    card_no = input("请输入 NFC 卡号：").strip().upper()
    person_type = input("请输入人员类型（正式工/三方/访客）：").strip()

    if not name or not employee_no or not card_no or not person_type:
        print("错误：姓名、工号、NFC 卡号和人员类型都不能为空")
        return
    allowed_types = {"正式工", "三方", "访客"}

    if person_type not in allowed_types:
        print("错误：人员类型只能是正式工、三方或访客")
        return
    new_person = {
        "name": name,
        "employee_no": employee_no,
        "card_no": card_no,
        "person_type": person_type,
        "is_active": True,
    }

    # people.append(new_person)
    # save_people(people)
    
    if employee_no_exists(people, new_person["employee_no"]):
        print("员工编号错误 已存在，无法新增")
        return

    if card_no_exists(people, new_person["card_no"]):
        print("NFC 卡号错误：已存在，无法新增")
        return
    people.append(new_person)
    save_people(people)

    print("新增并保存完成")


if __name__ == "__main__":
    main()