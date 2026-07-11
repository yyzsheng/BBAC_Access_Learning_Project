"""人员管理练习。

这个文件练习列表、字典、函数、循环、条件判断和用户输入。
后续正式项目会把这些数据放进数据库，但当前阶段先用列表模拟人员表。
"""


# 用列表保存多个人员；列表中的每一项都是一个人员字典。
people = [
    {
        "name": "张伟",
        "employee_no": "BBAC10001",
        "card_no": "0012345678",
        "person_type": "正式工",
        "is_active": True,
    },
    {
        "name": "李明",
        "employee_no": "TP20001",
        "card_no": "NFC-20001",
        "person_type": "三方",
        "is_active": True,
    },
]


def show_people(person_list):
    """显示人员列表。"""

    # len() 可以得到列表中人员的数量。
    print(f"当前共有 {len(person_list)} 人")

    # for 会逐个读取列表中的人员字典。
    for person in person_list:
        print(
            f"{person['name']} | "
            f"{person['employee_no']} | "
            f"{person['card_no']} | "
            f"{person['person_type']}"
        )


def find_person_by_employee_no(person_list, employee_no):
    """按照工号查找人员，找到时返回字典，找不到时返回 None。"""

    # 逐个人比较工号；工号是标识符，所以使用字符串比较。
    for person in person_list:
        if person["employee_no"] == employee_no:
            return person

    # None 表示没有找到，而不是返回一个假的人员字典。
    return None


def employee_no_exists(person_list, employee_no):
    """检查工号是否已经存在。"""

    # 找到重复工号后立即返回 True，避免继续无意义地遍历。
    for person in person_list:
        if person["employee_no"] == employee_no:
            return True

    # 遍历结束仍未找到，说明工号可以使用。
    return False


def card_no_exists(person_list, card_no):
    """检查 NFC 卡号是否已经存在。"""

    # 卡号也必须唯一，否则一张卡可能对应多个人员。
    for person in person_list:
        if person["card_no"] == card_no:
            return True

    return False


def add_person(person_list):
    """读取输入并新增人员，成功返回 True，失败返回 False。"""

    # strip() 可以去掉用户输入前后的空格，避免产生看不见的错误。
    name = input("请输入姓名：").strip()
    employee_no = input("请输入工号：").strip()
    card_no = input("请输入NFC卡号：").strip()
    person_type = input("请输入人员类型（正式工/三方/访客）：").strip()

    # 姓名、工号、卡号和人员类型都是必填字段。
    if not name or not employee_no or not card_no or not person_type:
        print("错误：姓名、工号、NFC卡号和人员类型都不能为空")
        return False

    # 限制人员类型，避免数据库中出现拼写不一致的数据。
    allowed_types = {"正式工", "三方", "访客"}
    if person_type not in allowed_types:
        print("错误：人员类型只能是正式工、三方或访客")
        return False

    # 工号不能重复，重复时直接结束本次新增。
    if employee_no_exists(person_list, employee_no):
        print("错误：这个工号已经存在")
        return False

    # NFC 卡号也不能重复，避免一张卡对应多个档案。
    if card_no_exists(person_list, card_no):
        print("错误：这个NFC卡号已经存在")
        return False

    # 校验全部通过后，才创建新的人员字典。
    new_person = {
        "name": name,
        "employee_no": employee_no,
        "card_no": card_no,
        "person_type": person_type,
        "is_active": True,
    }

    # append() 会把新字典添加到原来的人员列表中。
    person_list.append(new_person)
    print(f"人员 {name} 创建成功")
    return True


def search_person(person_list):
    """读取工号并显示查询结果。"""

    search_no = input("请输入要查询的员工编号：").strip()
    result = find_person_by_employee_no(person_list, search_no)

    if result is None:
        print("未找到该员工信息")
        return

    print(
        f"找到人员：{result['name']} | "
        f"{result['employee_no']} | "
        f"{result['card_no']} | "
        f"{result['person_type']}"
    )


def main():
    """程序入口：先显示、查询，再新增人员并重新显示。"""

    print("=== 初始人员列表 ===")
    show_people(people)

    print("\n=== 查询人员 ===")
    search_person(people)

    print("\n=== 新增人员 ===")
    created = add_person(people)

    # 只有新增成功时才重新显示列表。
    if created:
        print("\n=== 新增后的人员列表 ===")
        show_people(people)


# 只有直接运行这个文件时才执行 main()。
# 如果以后从其他文件导入函数，不会意外执行输入流程。
if __name__ == "__main__":
    main()
