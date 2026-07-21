"""刷卡记录模型自动检查练习。

这个文件先使用 Python 自带的 unittest，不额外安装 pytest。
目的不是追求复杂测试，而是让程序自动帮我们确认核心函数是否正常。
"""

import unittest

from backend.access_record_model import (
    AccessRecord,
    build_import_report,
    build_overview_summary,
    count_direction_records,
    find_records_by_date,
    find_records_by_employee_no,
    filter_records,
    get_present_people,
    remove_duplicate_records,
    sort_records_by_time,
    validate_access_record,
)


class AccessRecordModelTest(unittest.TestCase):
    """刷卡记录模型测试。"""

    def setUp(self):
        """每个测试运行前，准备一组固定测试数据。"""

        self.records = [
            AccessRecord(
                employee_no="BBAC10001",
                card_no="0012345678",
                name="张伟",
                campus="MRA",
                gate="MRA 总装主入口",
                direction="进",
                time="2026-07-19 09:30:00",
                result="通行成功",
            ),
            AccessRecord(
                employee_no="BBAC10001",
                card_no="0012345678",
                name="张伟",
                campus="MRA",
                gate="MRA 总装主入口",
                direction="出",
                time="2026-07-19 17:45:00",
                result="通行成功",
            ),
            AccessRecord(
                employee_no="BBAC10002",
                card_no="0012345679",
                name="李明",
                campus="PT1",
                gate="PT1 办公楼入口",
                direction="进",
                time="2026-07-19 09:35:00",
                result="通行成功",
            ),
        ]

    def test_valid_record_has_no_errors(self):
        record = self.records[0]

        errors = validate_access_record(record)

        self.assertEqual(errors, [])

    def test_wrong_campus_has_error(self):
        record = AccessRecord(
            employee_no="BBAC20003",
            card_no="0020000003",
            name="吴敏",
            campus="MRA1",
            gate="MRA1 临时门",
            direction="进",
            time="2026-07-20 08:15:00",
            result="通行成功",
        )

        errors = validate_access_record(record)

        self.assertIn("厂区只能是 MRA、PT1 或 PT2", errors)

    def test_count_direction_records(self):
        inbound_count, outbound_count = count_direction_records(self.records)

        self.assertEqual(inbound_count, 2)
        self.assertEqual(outbound_count, 1)

    def test_present_people_use_latest_record(self):
        present_people = get_present_people(self.records)
        present_employee_numbers = []

        for record in present_people:
            present_employee_numbers.append(record.employee_no)

        self.assertEqual(present_employee_numbers, ["BBAC10002"])

    def test_filter_records_by_campus_and_direction(self):
        matched_records = filter_records(
            self.records,
            date_text="2026-07-19",
            campus="MRA",
            direction="出",
        )

        self.assertEqual(len(matched_records), 1)
        self.assertEqual(matched_records[0].name, "张伟")

    def test_build_import_report(self):
        invalid_record = AccessRecord(
            employee_no="BBAC20003",
            card_no="0020000003",
            name="吴敏",
            campus="MRA1",
            gate="MRA1 临时门",
            direction="进",
            time="2026-07-20 08:15:00",
            result="通行成功",
        )

        valid_records, error_reports = build_import_report([self.records[0], invalid_record])

        self.assertEqual(len(valid_records), 1)
        self.assertEqual(len(error_reports), 1)
        self.assertEqual(error_reports[0]["row_number"], 3)

    def test_find_records_by_employee_no(self):
        matched_records = find_records_by_employee_no(self.records, "BBAC10001")

        self.assertEqual(len(matched_records), 2)
        self.assertEqual(matched_records[0].name, "张伟")

    def test_find_records_by_date(self):
        matched_records = find_records_by_date(self.records, "2026-07-19")

        self.assertEqual(len(matched_records), 3)

    def test_sort_records_by_time(self):
        unsorted_records = [
            self.records[1],
            self.records[2],
            self.records[0],
        ]

        sorted_records = sort_records_by_time(unsorted_records)

        self.assertEqual(sorted_records[0].time, "2026-07-19 09:30:00")
        self.assertEqual(sorted_records[-1].time, "2026-07-19 17:45:00")

    def test_remove_duplicate_records(self):
        duplicate_records = self.records + [self.records[0]]

        unique_records, duplicate_count = remove_duplicate_records(duplicate_records)

        self.assertEqual(len(unique_records), 3)
        self.assertEqual(duplicate_count, 1)

    def test_build_overview_summary(self):
        summary = build_overview_summary(self.records)

        self.assertEqual(summary["total_records"], 3)
        self.assertEqual(summary["inbound_count"], 2)
        self.assertEqual(summary["outbound_count"], 1)
        self.assertEqual(summary["present_count"], 1)
        self.assertEqual(summary["campus_present_counts"]["PT1"], 1)


if __name__ == "__main__":
    unittest.main()
