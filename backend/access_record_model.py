"""刷卡记录模型练习。

这个文件练习 dataclass、类型注解、字段校验和时间格式检查。
上一版 access_record.py 使用字典保存数据；这一版使用 AccessRecord 类保存数据。

为什么要学习模型：
- 字典很灵活，但字段名写错时 Python 不容易提前发现。
- 模型可以把一条业务数据需要哪些字段说清楚。
- 后续学习 Pydantic、FastAPI 和数据库模型时，都会用到类似思想。
"""

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


# 允许的厂区和进出方向集中放在常量中。
# 这样以后如果新增厂区，只需要改这里，不需要到处找代码。
ALLOWED_CAMPUSES = {"MRA", "PT1", "PT2"}
ALLOWED_DIRECTIONS = {"进", "出"}

# 这个文件专门保存本练习中校验通过的刷卡记录。
# 先不用原来的 access_records.json，避免影响之前的练习数据。
VALID_RECORDS_FILE = Path(__file__).parent / "valid_access_records.json"
CSV_RECORDS_FILE = Path(__file__).parent / "sample_access_records.csv"
CSV_IMPORT_ERRORS_FILE = Path(__file__).parent / "csv_import_errors.csv"


@dataclass
class AccessRecord:
    """一条刷卡记录。

    dataclass 会自动帮我们生成 __init__ 方法。
    所以创建对象时可以写：
    AccessRecord(employee_no="BBAC10001", ...)
    """

    employee_no: str
    card_no: str
    name: str
    campus: str
    gate: str
    direction: str
    time: str
    result: str


def validate_time_format(time_text):
    """检查时间是否符合 YYYY-MM-DD HH:MM:SS 格式。"""

    try:
        datetime.strptime(time_text, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False


def parse_record_time(record):
    """把记录里的时间字符串转换成 datetime 对象。

    字符串适合保存和显示，datetime 对象适合比较先后顺序。
    """

    return datetime.strptime(record.time, "%Y-%m-%d %H:%M:%S")


def validate_access_record(record):
    """校验一条刷卡记录，返回错误信息列表。

    如果返回空列表 []，表示校验通过。
    如果返回非空列表，里面每一项都是一个具体错误。
    """

    errors = []

    # 必填字段不能为空。strip() 可以避免只有空格的字符串通过校验。
    if not record.employee_no.strip():
        errors.append("工号不能为空")

    if not record.card_no.strip():
        errors.append("NFC 卡号不能为空")

    if not record.name.strip():
        errors.append("姓名不能为空")

    if not record.campus.strip():
        errors.append("厂区不能为空")

    if not record.gate.strip():
        errors.append("门禁点不能为空")

    # 厂区必须统一，否则后面统计 MRA/PT1/PT2 时会统计不准。
    if record.campus not in ALLOWED_CAMPUSES:
        errors.append("厂区只能是 MRA、PT1 或 PT2")

    # 方向必须统一成“进”和“出”，不能一会儿写“进入”，一会儿写“入场”。
    if record.direction not in ALLOWED_DIRECTIONS:
        errors.append("进出方向只能是“进”或“出”")

    # 时间格式必须统一，否则后面按日期查询、排序、统计会出问题。
    if not validate_time_format(record.time):
        errors.append("时间格式必须是 YYYY-MM-DD HH:MM:SS")

    return errors


def print_validation_result(record):
    """打印一条记录的校验结果。"""

    print(f"\n正在校验：{record.name} | {record.employee_no}")

    errors = validate_access_record(record)

    if not errors:
        print("校验通过")
        return

    print("校验失败：")
    for error in errors:
        print(f"- {error}")


def validate_records(record_list):
    """批量校验刷卡记录，返回通过数量和失败数量。

    这个函数练习“列表 + 循环 + 函数返回多个值”。
    后续导入 CSV/Excel 时，不会只校验一条记录，而是一次校验很多条记录。
    """

    success_count = 0
    failed_count = 0

    for record in record_list:
        errors = validate_access_record(record)

        if errors:
            failed_count += 1
        else:
            success_count += 1

    return success_count, failed_count


def record_to_dict(record):
    """把 AccessRecord 对象转换成字典。

    JSON 文件不能直接保存 AccessRecord 对象，但可以保存字典。
    asdict() 是 dataclasses 提供的工具，专门负责把 dataclass 对象变成字典。
    """

    return asdict(record)


def dict_to_record(record_dict):
    """把字典转换成 AccessRecord 对象。

    从 JSON 文件读出来的数据是字典。
    程序内部继续使用 AccessRecord 对象，这样后续校验和查询更统一。
    """

    return AccessRecord(
        employee_no=record_dict["employee_no"],
        card_no=record_dict["card_no"],
        name=record_dict["name"],
        campus=record_dict["campus"],
        gate=record_dict["gate"],
        direction=record_dict["direction"],
        time=record_dict["time"],
        result=record_dict["result"],
    )


def get_valid_record_dicts(record_list):
    """只取校验通过的记录，并转换成字典列表。

    后续保存 JSON 或导入数据库时，不能把错误数据直接保存进去。
    所以这里先过滤，再转换。
    """

    valid_record_dicts = []

    for record in record_list:
        errors = validate_access_record(record)

        if not errors:
            record_dict = record_to_dict(record)
            valid_record_dicts.append(record_dict)

    return valid_record_dicts


def save_valid_records(record_list):
    """把校验通过的刷卡记录保存到 JSON 文件。"""

    valid_record_dicts = get_valid_record_dicts(record_list)

    with VALID_RECORDS_FILE.open("w", encoding="utf-8") as file:
        json.dump(valid_record_dicts, file, ensure_ascii=False, indent=2)

    print(f"已保存 {len(valid_record_dicts)} 条有效记录到：{VALID_RECORDS_FILE}")


def save_records(record_list):
    """把传入的刷卡记录保存到 JSON 文件。

    这个函数默认调用方已经完成校验。
    它和 save_valid_records 的区别是：这里不会再次过滤，只负责保存。
    """

    record_dicts = []

    for record in record_list:
        record_dicts.append(record_to_dict(record))

    with VALID_RECORDS_FILE.open("w", encoding="utf-8") as file:
        json.dump(record_dicts, file, ensure_ascii=False, indent=2)

    print(f"已保存 {len(record_dicts)} 条记录到：{VALID_RECORDS_FILE}")


def load_saved_records():
    """从 JSON 文件读取刷卡记录，并转换成 AccessRecord 对象列表。"""

    if not VALID_RECORDS_FILE.exists():
        print("还没有保存过有效刷卡记录")
        return []

    with VALID_RECORDS_FILE.open("r", encoding="utf-8") as file:
        record_dicts = json.load(file)

    records = []

    for record_dict in record_dicts:
        record = dict_to_record(record_dict)
        records.append(record)

    print(f"已从 JSON 文件读取 {len(records)} 条记录")
    return records


def load_records_from_csv(csv_file):
    """从 CSV 文件读取刷卡记录，并转换成 AccessRecord 对象列表。

    CSV 文件的表头必须和 AccessRecord 字段名一致。
    当前练习先用小文件模拟，后续再处理真实 Excel/CSV 的字段映射。
    """

    records = []

    with csv_file.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            record = dict_to_record(row)
            records.append(record)

    print(f"已从 CSV 文件读取 {len(records)} 条记录")
    return records


def build_import_report(record_list):
    """生成导入报告：分出有效记录和错误明细。

    CSV 第 1 行是表头，所以第一条数据对应 CSV 第 2 行。
    错误明细里保留行号，方便用户回到原始文件修改。
    """

    valid_records = []
    error_reports = []

    for row_number, record in enumerate(record_list, start=2):
        errors = validate_access_record(record)

        if errors:
            error_reports.append(
                {
                    "row_number": row_number,
                    "employee_no": record.employee_no,
                    "name": record.name,
                    "errors": errors,
                }
            )
        else:
            valid_records.append(record)

    return valid_records, error_reports


def print_import_report(valid_records, error_reports):
    """打印 CSV 导入报告。"""

    print(f"可导入记录数：{len(valid_records)}")
    print(f"错误记录数：{len(error_reports)}")

    if not error_reports:
        print("没有导入错误")
        return

    print("错误明细：")
    for error_report in error_reports:
        print(
            f"第 {error_report['row_number']} 行 | "
            f"{error_report['employee_no']} | "
            f"{error_report['name']}"
        )

        for error in error_report["errors"]:
            print(f"- {error}")


def save_import_errors(error_reports):
    """把 CSV 导入错误明细保存成 CSV 文件。

    后续做 Web 系统时，管理员导入失败后，可以下载类似的错误明细文件。
    """

    if not error_reports:
        print("没有错误明细需要保存")
        return

    with CSV_IMPORT_ERRORS_FILE.open("w", encoding="utf-8", newline="") as file:
        fieldnames = ["row_number", "employee_no", "name", "errors"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for error_report in error_reports:
            writer.writerow(
                {
                    "row_number": error_report["row_number"],
                    "employee_no": error_report["employee_no"],
                    "name": error_report["name"],
                    "errors": "；".join(error_report["errors"]),
                }
            )

    print(f"错误明细已保存到：{CSV_IMPORT_ERRORS_FILE}")


def get_record_unique_key(record):
    """生成一条刷卡记录的唯一标识。

    当前阶段先用这些字段判断是否重复：
    工号 + 卡号 + 门点 + 方向 + 时间。
    后续进入数据库后，会把类似规则做成唯一约束。
    """

    return (
        record.employee_no,
        record.card_no,
        record.gate,
        record.direction,
        record.time,
    )


def remove_duplicate_records(record_list):
    """去除重复刷卡记录，保留第一次出现的记录。"""

    unique_records = []
    seen_keys = set()
    duplicate_count = 0

    for record in record_list:
        record_key = get_record_unique_key(record)

        if record_key in seen_keys:
            duplicate_count += 1
            continue

        seen_keys.add(record_key)
        unique_records.append(record)

    return unique_records, duplicate_count


def import_valid_csv_records(saved_records, csv_records):
    """把 CSV 中校验通过的记录追加到现有记录中。

    错误记录不会写入 JSON。
    重复记录不会重复写入 JSON。
    返回导入后的完整记录列表、错误报告和重复记录数量。
    """

    valid_csv_records, error_reports = build_import_report(csv_records)
    imported_records = saved_records + valid_csv_records
    imported_records, duplicate_count = remove_duplicate_records(imported_records)

    save_records(imported_records)

    return imported_records, error_reports, duplicate_count


def print_duplicate_check_result(record_list):
    """打印重复记录检查结果。"""

    unique_records, duplicate_count = remove_duplicate_records(record_list)
    print(f"原始记录数：{len(record_list)}")
    print(f"去重后记录数：{len(unique_records)}")
    print(f"重复记录数：{duplicate_count}")


def find_records_by_employee_no(record_list, employee_no):
    """按照工号查询刷卡记录。

    一个员工可能有多条刷卡记录，所以返回列表。
    如果没有找到，返回空列表 []。
    """

    matched_records = []

    for record in record_list:
        if record.employee_no == employee_no:
            matched_records.append(record)

    return matched_records


def find_records_by_date(record_list, date_text):
    """按照日期查询刷卡记录。

    date_text 格式使用 YYYY-MM-DD，例如 2026-07-19。
    record.time 是 YYYY-MM-DD HH:MM:SS，所以前 10 个字符就是日期。
    """

    matched_records = []

    for record in record_list:
        record_date = record.time[:10]

        if record_date == date_text:
            matched_records.append(record)

    return matched_records


def find_records_by_campus(record_list, campus):
    """按照厂区查询刷卡记录。"""

    matched_records = []

    for record in record_list:
        if record.campus == campus:
            matched_records.append(record)

    return matched_records


def filter_records(record_list, date_text="", campus="", direction=""):
    """按多个条件筛选刷卡记录。

    这里用空字符串表示“不筛选这个条件”。
    例如：
    - date_text="2026-07-19" 表示只看这一天
    - campus="MRA" 表示只看 MRA
    - direction="进" 表示只看进场记录
    """

    matched_records = []

    for record in record_list:
        if date_text and record.time[:10] != date_text:
            continue

        if campus and record.campus != campus:
            continue

        if direction and record.direction != direction:
            continue

        matched_records.append(record)

    return matched_records


def print_record_list(record_list):
    """打印刷卡记录列表。"""

    if not record_list:
        print("没有找到刷卡记录")
        return

    print(f"找到 {len(record_list)} 条刷卡记录")

    for record in record_list:
        print(
            f"{record.time} | "
            f"{record.name} | "
            f"{record.employee_no} | "
            f"{record.campus} | "
            f"{record.gate} | "
            f"{record.direction}"
        )


def count_direction_records(record_list):
    """统计进场和出场记录数量。

    这里统计的是记录次数，不是人数。
    例如同一个人一天进出多次，会按多条刷卡记录计算。
    """

    inbound_count = 0
    outbound_count = 0

    for record in record_list:
        if record.direction == "进":
            inbound_count += 1
        elif record.direction == "出":
            outbound_count += 1

    return inbound_count, outbound_count


def sort_records_by_time(record_list):
    """按照刷卡时间从早到晚排序。"""

    return sorted(record_list, key=parse_record_time)


def get_latest_records_by_employee(record_list):
    """找出每个员工最后一条刷卡记录。

    返回一个字典：
    - key 是工号
    - value 是这个工号最后一次刷卡记录

    这里会先按刷卡时间排序，避免原始数据顺序混乱时判断错误。
    """

    latest_records = {}
    sorted_records = sort_records_by_time(record_list)

    for record in sorted_records:
        latest_records[record.employee_no] = record

    return latest_records


def get_present_people(record_list):
    """根据每个人最后一条刷卡记录，计算当前在场人员。"""

    present_people = []
    latest_records = get_latest_records_by_employee(record_list)

    for record in latest_records.values():
        if record.direction == "进":
            present_people.append(record)

    return present_people


def count_present_people_by_campus(record_list):
    """按厂区统计当前在场人数。"""

    campus_counts = {
        "MRA": 0,
        "PT1": 0,
        "PT2": 0,
    }
    present_people = get_present_people(record_list)

    for record in present_people:
        campus_counts[record.campus] += 1

    return campus_counts


def build_overview_summary(record_list):
    """生成门禁记录总览摘要。

    这个函数只负责计算数据，不负责打印。
    后续做网页接口时，类似函数可以直接返回给前端页面使用。
    """

    inbound_count, outbound_count = count_direction_records(record_list)
    present_people = get_present_people(record_list)
    campus_counts = count_present_people_by_campus(record_list)

    return {
        "total_records": len(record_list),
        "inbound_count": inbound_count,
        "outbound_count": outbound_count,
        "present_count": len(present_people),
        "campus_present_counts": campus_counts,
    }


def print_overview_summary(summary):
    """打印门禁记录总览摘要。"""

    print(f"总刷卡记录数：{summary['total_records']}")
    print(f"进场次数：{summary['inbound_count']}")
    print(f"出场次数：{summary['outbound_count']}")
    print(f"当前在场人数：{summary['present_count']}")
    print("各厂区当前在场人数：")

    for campus, count in summary["campus_present_counts"].items():
        print(f"- {campus}：{count}")


def main():
    """程序入口：准备三条测试数据并逐条校验。"""

    correct_record = AccessRecord(
        employee_no="BBAC10001",
        card_no="0012345678",
        name="张伟",
        campus="MRA",
        gate="MRA 总装主入口",
        direction="进",
        time="2026-07-19 09:30:00",
        result="通行成功",
    )

    second_record = AccessRecord(
        employee_no="BBAC10002",
        card_no="0012345679",
        name="李明",
        campus="PT1",
        gate="PT1 办公楼入口",
        direction="进",
        time="2026-07-19 09:35:00",
        result="通行成功",
    )

    third_record = AccessRecord(
        employee_no="BBAC10003",
        card_no="0012345680",
        name="王强",
        campus="MRA",
        gate="MRA 东门",
        direction="出",
        time="2026-07-19 18:10:00",
        result="通行成功",
    )

    fourth_record = AccessRecord(
        employee_no="BBAC10004",
        card_no="0012345681",
        name="赵敏",
        campus="PT2",
        gate="PT2 北门",
        direction="进",
        time="2026-07-19 08:20:00",
        result="通行成功",
    )

    zhang_wei_out_record = AccessRecord(
        employee_no="BBAC10001",
        card_no="0012345678",
        name="张伟",
        campus="MRA",
        gate="MRA 总装主入口",
        direction="出",
        time="2026-07-19 17:45:00",
        result="通行成功",
    )

    records = [
        correct_record,
        second_record,
        third_record,
        fourth_record,
        zhang_wei_out_record,
    ]

    for record in records:
        print_validation_result(record)

    print("\n=== 批量校验统计 ===")
    success_count, failed_count = validate_records(records)
    print(f"总记录数：{len(records)}")
    print(f"校验通过：{success_count}")
    print(f"校验失败：{failed_count}")

    print("\n=== 可保存的记录字典 ===")
    valid_record_dicts = get_valid_record_dicts(records)
    for record_dict in valid_record_dicts:
        print(record_dict)

    print("\n=== 保存有效记录 ===")
    save_valid_records(records)

    print("\n=== 从 JSON 读回记录 ===")
    saved_records = load_saved_records()
    for record in saved_records:
        print(f"{record.time} | {record.name} | {record.campus} | {record.direction}")

    print("\n=== 从 CSV 导入记录 ===")
    csv_records = load_records_from_csv(CSV_RECORDS_FILE)
    for record in csv_records:
        print_validation_result(record)

    print("\n=== CSV 有效记录统计 ===")
    success_count, failed_count = validate_records(csv_records)
    print(f"CSV 总记录数：{len(csv_records)}")
    print(f"CSV 校验通过：{success_count}")
    print(f"CSV 校验失败：{failed_count}")

    print("\n=== CSV 导入错误报告 ===")
    valid_csv_records, csv_error_reports = build_import_report(csv_records)
    print_import_report(valid_csv_records, csv_error_reports)

    print("\n=== 保存 CSV 导入错误明细 ===")
    save_import_errors(csv_error_reports)

    print("\n=== 导入 CSV 有效记录到 JSON ===")
    imported_records, csv_error_reports, duplicate_count = import_valid_csv_records(
        saved_records,
        csv_records,
    )
    print(f"导入后总记录数：{len(imported_records)}")
    print(f"本次跳过错误记录数：{len(csv_error_reports)}")
    print(f"本次跳过重复记录数：{duplicate_count}")

    print("\n=== 重复记录检查演示 ===")
    duplicate_demo_records = imported_records + [imported_records[0]]
    print_duplicate_check_result(duplicate_demo_records)

    print("\n=== 按时间排序后的记录 ===")
    sorted_records = sort_records_by_time(imported_records)
    for record in sorted_records:
        print(f"{record.time} | {record.name} | {record.direction}")

    print("\n=== 按工号查询：BBAC10001 ===")
    matched_records = find_records_by_employee_no(imported_records, "BBAC10001")
    print_record_list(matched_records)

    print("\n=== 按工号查询：NOT_EXIST ===")
    matched_records = find_records_by_employee_no(imported_records, "NOT_EXIST")
    print_record_list(matched_records)

    print("\n=== 按日期查询：2026-07-19 ===")
    matched_records = find_records_by_date(imported_records, "2026-07-19")
    print_record_list(matched_records)

    print("\n=== 按日期查询：2026-07-20 ===")
    matched_records = find_records_by_date(imported_records, "2026-07-20")
    print_record_list(matched_records)

    print("\n=== 按厂区查询：MRA ===")
    matched_records = find_records_by_campus(imported_records, "MRA")
    print_record_list(matched_records)

    print("\n=== 按厂区查询：PT2 ===")
    matched_records = find_records_by_campus(imported_records, "PT2")
    print_record_list(matched_records)

    print("\n=== 组合筛选：2026-07-19 + MRA + 进 ===")
    matched_records = filter_records(
        imported_records,
        date_text="2026-07-19",
        campus="MRA",
        direction="进",
    )
    print_record_list(matched_records)

    print("\n=== 组合筛选：2026-07-19 + MRA + 出 ===")
    matched_records = filter_records(
        imported_records,
        date_text="2026-07-19",
        campus="MRA",
        direction="出",
    )
    print_record_list(matched_records)

    print("\n=== 进出次数统计 ===")
    inbound_count, outbound_count = count_direction_records(imported_records)
    print(f"进场次数：{inbound_count}")
    print(f"出场次数：{outbound_count}")

    print("\n=== 当前在场人员 ===")
    present_people = get_present_people(imported_records)
    print(f"当前在场人数：{len(present_people)}")
    print_record_list(present_people)

    print("\n=== 各厂区当前在场人数 ===")
    campus_counts = count_present_people_by_campus(imported_records)
    for campus, count in campus_counts.items():
        print(f"{campus}：{count}")

    print("\n=== 门禁记录总览摘要 ===")
    overview_summary = build_overview_summary(imported_records)
    print_overview_summary(overview_summary)


if __name__ == "__main__":
    main()
