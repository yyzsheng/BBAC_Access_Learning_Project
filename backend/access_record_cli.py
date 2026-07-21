"""刷卡记录命令行菜单。

这个文件把 access_record_model.py 里的函数组装成一个可操作的小系统。
模型文件负责“业务能力”，这个文件负责“用户怎么选择功能”。
"""

from access_record_model import (
    CSV_RECORDS_FILE,
    build_import_report,
    build_overview_summary,
    find_records_by_campus,
    find_records_by_date,
    find_records_by_employee_no,
    filter_records,
    count_present_people_by_campus,
    get_present_people,
    import_valid_csv_records,
    load_records_from_csv,
    load_saved_records,
    print_import_report,
    print_overview_summary,
    print_record_list,
    save_import_errors,
)


def print_menu():
    """显示命令行菜单。"""

    print("\n=== BBAC 门禁刷卡记录菜单 ===")
    print("1. 查看总览摘要")
    print("2. 按工号查询")
    print("3. 按日期查询")
    print("4. 按厂区查询")
    print("5. 导入示例 CSV")
    print("6. 组合筛选")
    print("7. 查看当前在场人员")
    print("8. 查看各厂区在场人数")
    print("0. 退出")


def handle_overview(records):
    """处理总览摘要功能。"""

    summary = build_overview_summary(records)
    print_overview_summary(summary)


def handle_employee_search(records):
    """处理按工号查询功能。"""

    employee_no = input("请输入工号：").strip()
    matched_records = find_records_by_employee_no(records, employee_no)
    print_record_list(matched_records)


def handle_date_search(records):
    """处理按日期查询功能。"""

    date_text = input("请输入日期（YYYY-MM-DD）：").strip()
    matched_records = find_records_by_date(records, date_text)
    print_record_list(matched_records)


def handle_campus_search(records):
    """处理按厂区查询功能。"""

    campus = input("请输入厂区（MRA/PT1/PT2）：").strip()
    matched_records = find_records_by_campus(records, campus)
    print_record_list(matched_records)


def handle_csv_import(records):
    """处理示例 CSV 导入功能。"""

    csv_records = load_records_from_csv(CSV_RECORDS_FILE)
    valid_csv_records, error_reports = build_import_report(csv_records)

    print("\n=== CSV 导入报告 ===")
    print_import_report(valid_csv_records, error_reports)

    print("\n=== 保存错误明细 ===")
    save_import_errors(error_reports)

    imported_records, error_reports, duplicate_count = import_valid_csv_records(
        records,
        csv_records,
    )

    print(f"导入后总记录数：{len(imported_records)}")
    print(f"跳过错误记录数：{len(error_reports)}")
    print(f"跳过重复记录数：{duplicate_count}")

    return imported_records


def handle_combined_filter(records):
    """处理组合筛选功能。"""

    print("如果某个条件不想筛选，直接按回车跳过")
    date_text = input("请输入日期（YYYY-MM-DD）：").strip()
    campus = input("请输入厂区（MRA/PT1/PT2）：").strip()
    direction = input("请输入方向（进/出）：").strip()

    matched_records = filter_records(
        records,
        date_text=date_text,
        campus=campus,
        direction=direction,
    )
    print_record_list(matched_records)


def handle_present_people(records):
    """处理当前在场人员查询功能。"""

    present_people = get_present_people(records)
    print(f"当前在场人数：{len(present_people)}")
    print_record_list(present_people)


def handle_present_count_by_campus(records):
    """处理各厂区当前在场人数查询功能。"""

    campus_counts = count_present_people_by_campus(records)

    for campus, count in campus_counts.items():
        print(f"{campus}：{count}")


def main():
    """程序入口：循环显示菜单，直到用户选择退出。"""

    records = load_saved_records()

    while True:
        print_menu()
        choice = input("请输入选项：").strip()

        if choice == "1":
            handle_overview(records)
        elif choice == "2":
            handle_employee_search(records)
        elif choice == "3":
            handle_date_search(records)
        elif choice == "4":
            handle_campus_search(records)
        elif choice == "5":
            records = handle_csv_import(records)
        elif choice == "6":
            handle_combined_filter(records)
        elif choice == "7":
            handle_present_people(records)
        elif choice == "8":
            handle_present_count_by_campus(records)
        elif choice == "0":
            print("程序已退出")
            break
        else:
            print("错误：未知选项")


if __name__ == "__main__":
    main()
