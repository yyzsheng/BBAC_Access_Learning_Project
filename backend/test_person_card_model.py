"""人员与卡片模型自动检查练习。"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from backend.person_card_model import (
    Card,
    Person,
    add_card,
    add_person,
    build_people_summary,
    find_card_by_card_no,
    find_people_by_name_keyword,
    find_person_by_employee_no,
    load_people_and_cards,
    save_people_and_cards,
    validate_card,
    validate_person,
)


class PersonCardModelTest(unittest.TestCase):
    """人员与卡片模型测试。"""

    def setUp(self):
        self.people = [
            Person(
                employee_no="BBAC10001",
                name="张伟",
                person_type="正式工",
                organization="总装车间",
                campus="MRA",
            ),
            Person(
                employee_no="TP20001",
                name="李明",
                person_type="三方",
                organization="保洁供应商",
                campus="PT1",
            ),
        ]
        self.cards = [
            Card(
                card_no="CARD10001",
                employee_no="BBAC10001",
            )
        ]

    def test_valid_person_has_no_errors(self):
        errors = validate_person(self.people[0])

        self.assertEqual(errors, [])

    def test_invalid_person_type_has_error(self):
        person = Person(
            employee_no="BBAC99999",
            name="测试",
            person_type="外包",
            organization="测试组织",
            campus="MRA",
        )

        errors = validate_person(person)

        self.assertIn("人员类型只能是正式工、三方或访客", errors)

    def test_valid_card_has_no_errors(self):
        errors = validate_card(self.cards[0])

        self.assertEqual(errors, [])

    def test_add_person_success(self):
        person = Person(
            employee_no="VIS30001",
            name="访客甲",
            person_type="访客",
            organization="访客单位",
            campus="PT2",
        )

        success, errors = add_person(self.people, person)

        self.assertTrue(success)
        self.assertEqual(errors, [])
        self.assertEqual(len(self.people), 3)

    def test_add_person_duplicate_employee_no_fails(self):
        person = Person(
            employee_no="BBAC10001",
            name="重复人员",
            person_type="正式工",
            organization="总装车间",
            campus="MRA",
        )

        success, errors = add_person(self.people, person)

        self.assertFalse(success)
        self.assertIn("工号已经存在", errors)

    def test_add_card_success(self):
        card = Card(
            card_no="CARD20001",
            employee_no="TP20001",
        )

        success, errors = add_card(self.cards, self.people, card)

        self.assertTrue(success)
        self.assertEqual(errors, [])
        self.assertEqual(len(self.cards), 2)

    def test_add_card_unknown_employee_fails(self):
        card = Card(
            card_no="CARD99999",
            employee_no="NOT_EXIST",
        )

        success, errors = add_card(self.cards, self.people, card)

        self.assertFalse(success)
        self.assertIn("绑定工号不存在", errors)

    def test_find_person_by_employee_no(self):
        person = find_person_by_employee_no(self.people, "bbac10001")

        self.assertEqual(person.name, "张伟")

    def test_find_people_by_name_keyword(self):
        matched_people = find_people_by_name_keyword(self.people, "李")

        self.assertEqual(len(matched_people), 1)
        self.assertEqual(matched_people[0].employee_no, "TP20001")

    def test_find_card_by_card_no(self):
        card = find_card_by_card_no(self.cards, "card10001")

        self.assertEqual(card.employee_no, "BBAC10001")

    def test_build_people_summary(self):
        summary = build_people_summary(self.people, self.cards)

        self.assertEqual(summary["total_people"], 2)
        self.assertEqual(summary["active_people"], 2)
        self.assertEqual(summary["total_cards"], 1)
        self.assertEqual(summary["person_type_counts"]["正式工"], 1)
        self.assertEqual(summary["person_type_counts"]["三方"], 1)

    def test_save_and_load_people_and_cards(self):
        with TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "people_cards.json"

            save_people_and_cards(self.people, self.cards, data_file=data_file)
            loaded_people, loaded_cards = load_people_and_cards(data_file=data_file)

        self.assertEqual(len(loaded_people), 2)
        self.assertEqual(len(loaded_cards), 1)
        self.assertEqual(loaded_people[0].name, "张伟")
        self.assertEqual(loaded_cards[0].card_no, "CARD10001")


if __name__ == "__main__":
    unittest.main()
