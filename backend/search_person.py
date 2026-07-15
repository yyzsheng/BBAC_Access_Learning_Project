from person_json_safe import load_people


def find_person_by_employee_no(people, employee_no):
    for person in people:
        if person["employee_no"].upper() == employee_no.upper():
            return person
    return None

def find_people_by_name_keyword(people, keyword):
    result = []

    for person in people:
        if keyword in person["name"]:
            result.append(person)

    return result

def print_person(person):
    print(person["name"], person["employee_no"], person["card_no"], person["person_type"])


def main():
    people = load_people()

    print("请选择查询方式：")
    print("1. 按工号查询")
    print("2. 按姓名关键字查询")

    choice = input("请输入选项：").strip()

    if choice == "1":
        employee_no = input("请输入要查询的工号：").strip().upper()
        person = find_person_by_employee_no(people, employee_no)

        if person is None:
            print("未找到该人员")
            return

        print("找到人员：")
        print_person(person)  
        return

    if choice == "2":
        keyword = input("请输入姓名关键字：").strip()
        matched_people = find_people_by_name_keyword(people, keyword)

        if not matched_people:
            print("未找到匹配人员")
            return

        print(f"找到 {len(matched_people)} 人：")
        for person in matched_people:
            print_person(person)
        return

    print("错误：未知选项")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已退出")