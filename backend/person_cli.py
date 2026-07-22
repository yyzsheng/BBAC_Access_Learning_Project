"""人员与卡片命令行菜单。"""

from person_card_model import (
    Card,
    Person,
    add_card,
    add_person,
    build_people_summary,
    find_card_by_card_no,
    find_people_by_name_keyword,
    find_person_by_employee_no,
    load_people_and_cards,
    print_people_summary,
    save_people_and_cards,
)


def print_menu():
    """显示人员与卡片菜单。"""

    print("\n=== BBAC 人员与卡片菜单 ===")
    print("1. 查看人员与卡片摘要")
    print("2. 新增人员")
    print("3. 绑定卡片")
    print("4. 按工号查询人员")
    print("5. 按姓名关键字查询人员")
    print("6. 按卡号查询卡片")
    print("0. 退出")


def print_person(person):
    """打印人员。"""

    print(
        f"{person.employee_no} | "
        f"{person.name} | "
        f"{person.person_type} | "
        f"{person.organization} | "
        f"{person.campus} | "
        f"启用：{person.is_active}"
    )


def print_card(card):
    """打印卡片。"""

    print(
        f"{card.card_no} | "
        f"绑定工号：{card.employee_no} | "
        f"启用：{card.is_active}"
    )


def print_errors(errors):
    """打印错误信息。"""

    for error in errors:
        print(f"- {error}")


def handle_summary(people, cards):
    """处理摘要功能。"""

    summary = build_people_summary(people, cards)
    print_people_summary(summary)


def handle_add_person(people, cards):
    """处理新增人员功能。"""

    person = Person(
        employee_no=input("请输入工号：").strip(),
        name=input("请输入姓名：").strip(),
        person_type=input("请输入人员类型（正式工/三方/访客）：").strip(),
        organization=input("请输入组织：").strip(),
        campus=input("请输入厂区：").strip(),
    )

    success, errors = add_person(people, person)

    if not success:
        print("新增人员失败：")
        print_errors(errors)
        return

    save_people_and_cards(people, cards)
    print("新增人员成功")


def handle_add_card(people, cards):
    """处理绑定卡片功能。"""

    card = Card(
        card_no=input("请输入卡号：").strip(),
        employee_no=input("请输入绑定工号：").strip(),
    )

    success, errors = add_card(cards, people, card)

    if not success:
        print("绑定卡片失败：")
        print_errors(errors)
        return

    save_people_and_cards(people, cards)
    print("绑定卡片成功")


def handle_search_person_by_employee_no(people):
    """处理按工号查询人员功能。"""

    employee_no = input("请输入工号：").strip()
    person = find_person_by_employee_no(people, employee_no)

    if person is None:
        print("未找到人员")
        return

    print_person(person)


def handle_search_people_by_name(people):
    """处理按姓名关键字查询人员功能。"""

    keyword = input("请输入姓名关键字：").strip()
    matched_people = find_people_by_name_keyword(people, keyword)

    if not matched_people:
        print("未找到人员")
        return

    print(f"找到 {len(matched_people)} 人")
    for person in matched_people:
        print_person(person)


def handle_search_card(cards):
    """处理按卡号查询卡片功能。"""

    card_no = input("请输入卡号：").strip()
    card = find_card_by_card_no(cards, card_no)

    if card is None:
        print("未找到卡片")
        return

    print_card(card)


def main():
    """程序入口。"""

    people, cards = load_people_and_cards()

    while True:
        print_menu()
        choice = input("请输入选项：").strip()

        if choice == "1":
            handle_summary(people, cards)
        elif choice == "2":
            handle_add_person(people, cards)
        elif choice == "3":
            handle_add_card(people, cards)
        elif choice == "4":
            handle_search_person_by_employee_no(people)
        elif choice == "5":
            handle_search_people_by_name(people)
        elif choice == "6":
            handle_search_card(cards)
        elif choice == "0":
            print("程序已退出")
            break
        else:
            print("错误：未知选项")


if __name__ == "__main__":
    main()
