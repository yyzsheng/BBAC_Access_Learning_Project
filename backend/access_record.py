"""门禁刷卡记录练习。

这个文件练习 JSON 文件、列表、字典、函数、时间和统计。
当前使用 JSON 模拟数据库，后续正式项目会改为 MySQL。
"""

import json
from datetime import datetime
from pathlib import Path


# 数据文件放在当前 Python 文件所在的 backend 文件夹中。
# 使用 Path(__file__) 可以避免因为运行目录不同而找不到文件。
DATA_FILE = Path(__file__).parent / "access_records.json"


def save_records(record_list):
    """把刷卡记录列表保存到 JSON 文件。"""

    # 使用 w 模式写入文件；如果文件不存在，Python 会自动创建它。
    with DATA_FILE.open("w", encoding="utf-8") as file:
        # ensure_ascii=False 保证中文正常保存，indent=2 让文件容易阅读。
        json.dump(record_list, file, ensure_ascii=False, indent=2)

    print(f"刷卡记录已保存到：{DATA_FILE}")


def load_records():
    """从 JSON 文件读取刷卡记录；文件不存在时返回空列表。"""

    # 第一次运行时文件可能还不存在，所以要先判断。
    if not DATA_FILE.exists():
        print(f"{DATA_FILE} 不存在，使用空记录列表")
        return []

    # 使用 r 模式读取已有数据。
    with DATA_FILE.open("r", encoding="utf-8") as file:
        records = json.load(file)

    print(f"已从 {DATA_FILE} 加载 {len(records)} 条刷卡记录")
    return records


def show_records(record_list):
    """显示刷卡记录列表。"""

    # 没有记录时给出明确提示，避免用户误以为程序没有运行。
    if not record_list:
        print("当前没有刷卡记录")
        return

    print(f"当前共有 {len(record_list)} 条刷卡记录")

    # 逐条显示记录中的关键字段。
    for record in record_list:
        print(
            f"{record['time']} | "
            f"{record['name']} | "
            f"{record['employee_no']} | "
            f"{record['campus']} | "
            f"{record['gate']} | "
            f"{record['direction']} | "
            f"{record['result']}"
        )


def add_record(record_list):
    """通过输入新增一条刷卡记录，成功返回 True，失败返回 False。"""

    # strip() 用于去除用户输入前后的空格。
    name = input("请输入姓名：").strip()
    employee_no = input("请输入员工编号：").strip()
    card_no = input("请输入 NFC 卡号：").strip()
    campus = input("请输入厂区（MRA/PT1/PT2）：").strip()
    gate = input("请输入逻辑门禁点：").strip()
    direction = input("请输入进出方向（进/出）：").strip()
    result = input("请输入刷卡结果：").strip() or "通行成功"

    # 这些字段不能为空，否则记录无法用于后续查询和统计。
    if not name or not employee_no or not card_no or not campus or not gate:
        print("错误：姓名、工号、卡号、厂区和门禁点不能为空")
        return False

    # 方向只有两个合法值，避免出现“进入”“离开”等不统一的文字。
    if direction not in {"进", "出"}:
        print("错误：进出方向只能填写“进”或“出”")
        return False

    # 使用当前时间生成一条新的刷卡时间。
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 将输入内容整理成一条结构统一的字典记录。
    new_record = {
        "employee_no": employee_no,
        "card_no": card_no,
        "name": name,
        "campus": campus,
        "gate": gate,
        "direction": direction,
        "time": current_time,
        "result": result,
    }

    # append() 把新记录添加到原来的列表中。
    record_list.append(new_record)
    print("刷卡记录添加成功")
    return True


def find_records_by_employee_no(record_list, employee_no):
    """按照工号查找记录，返回匹配记录组成的新列表。"""

    # 一个员工可以有很多条刷卡记录，所以返回列表而不是单个字典。
    result = []

    for record in record_list:
        if record["employee_no"] == employee_no:
            result.append(record)

    return result


def count_directions(record_list):
    """统计记录中的进场和出场数量。"""

    # 分别使用两个计数器统计“进”和“出”。
    inbound = 0
    outbound = 0

    for record in record_list:
        if record["direction"] == "进":
            inbound += 1
        elif record["direction"] == "出":
            outbound += 1

    # 返回两个结果，调用方可以分别接收。
    return inbound, outbound


def main():
    """程序入口：读取、显示、新增、查询和统计刷卡记录。"""

    # 程序启动时先从 JSON 文件恢复历史记录。
    records = load_records()

    print("\n=== 当前刷卡记录 ===")
    show_records(records)

    print("\n=== 新增刷卡记录 ===")
    created = add_record(records)

    # 只有新增成功后才保存，避免把错误数据写入文件。
    if created:
        save_records(records)

    print("\n=== 当前进出统计 ===")
    inbound, outbound = count_directions(records)
    print(f"进场次数：{inbound}")
    print(f"出场次数：{outbound}")

    print("\n=== 按工号查询 ===")
    search_employee_no = input("请输入要查询的工号：").strip()
    matched_records = find_records_by_employee_no(records, search_employee_no)

    # 根据查询结果数量显示不同提示。
    if matched_records:
        print(f"找到 {len(matched_records)} 条记录")
        show_records(matched_records)
    else:
        print("没有找到该工号的刷卡记录")


# 只有直接运行本文件时才执行 main()。
# 如果以后从其他文件导入函数，不会自动执行输入流程。
if __name__ == "__main__":
    main()
