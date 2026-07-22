"""人员与卡片模型练习。

第一阶段最终需要同时管理人员、卡片和刷卡记录。
这个文件负责人员和卡片的基础模型、校验、查询和 JSON 保存。
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path


ALLOWED_PERSON_TYPES = {"正式工", "三方", "访客"}
PEOPLE_STORE_FILE = Path(__file__).parent / "phase1_people.json"


@dataclass
class Person:
    """人员档案。"""

    employee_no: str
    name: str
    person_type: str
    organization: str
    campus: str
    is_active: bool = True


@dataclass
class Card:
    """NFC 卡片档案。"""

    card_no: str
    employee_no: str
    is_active: bool = True


def validate_person(person):
    """校验人员档案，返回错误信息列表。"""

    errors = []

    if not person.employee_no.strip():
        errors.append("工号不能为空")

    if not person.name.strip():
        errors.append("姓名不能为空")

    if person.person_type not in ALLOWED_PERSON_TYPES:
        errors.append("人员类型只能是正式工、三方或访客")

    if not person.organization.strip():
        errors.append("组织不能为空")

    if not person.campus.strip():
        errors.append("厂区不能为空")

    return errors


def validate_card(card):
    """校验卡片档案，返回错误信息列表。"""

    errors = []

    if not card.card_no.strip():
        errors.append("卡号不能为空")

    if not card.employee_no.strip():
        errors.append("绑定工号不能为空")

    return errors


def person_to_dict(person):
    """把 Person 对象转换成字典。"""

    return asdict(person)


def card_to_dict(card):
    """把 Card 对象转换成字典。"""

    return asdict(card)


def dict_to_person(person_dict):
    """把字典转换成 Person 对象。"""

    return Person(
        employee_no=person_dict["employee_no"],
        name=person_dict["name"],
        person_type=person_dict["person_type"],
        organization=person_dict["organization"],
        campus=person_dict["campus"],
        is_active=person_dict.get("is_active", True),
    )


def dict_to_card(card_dict):
    """把字典转换成 Card 对象。"""

    return Card(
        card_no=card_dict["card_no"],
        employee_no=card_dict["employee_no"],
        is_active=card_dict.get("is_active", True),
    )


def find_person_by_employee_no(people, employee_no):
    """按工号查询人员。"""

    for person in people:
        if person.employee_no.upper() == employee_no.upper():
            return person

    return None


def find_people_by_name_keyword(people, keyword):
    """按姓名关键字查询人员。"""

    matched_people = []

    for person in people:
        if keyword in person.name:
            matched_people.append(person)

    return matched_people


def find_card_by_card_no(cards, card_no):
    """按卡号查询卡片。"""

    for card in cards:
        if card.card_no.upper() == card_no.upper():
            return card

    return None


def employee_no_exists(people, employee_no):
    """检查工号是否已存在。"""

    return find_person_by_employee_no(people, employee_no) is not None


def card_no_exists(cards, card_no):
    """检查卡号是否已存在。"""

    return find_card_by_card_no(cards, card_no) is not None


def add_person(people, person):
    """新增人员。成功返回 True，失败返回 False 和错误列表。"""

    errors = validate_person(person)

    if employee_no_exists(people, person.employee_no):
        errors.append("工号已经存在")

    if errors:
        return False, errors

    people.append(person)
    return True, []


def add_card(cards, people, card):
    """新增卡片。成功返回 True，失败返回 False 和错误列表。"""

    errors = validate_card(card)

    if card_no_exists(cards, card.card_no):
        errors.append("卡号已经存在")

    if find_person_by_employee_no(people, card.employee_no) is None:
        errors.append("绑定工号不存在")

    if errors:
        return False, errors

    cards.append(card)
    return True, []


def save_people_and_cards(people, cards, data_file=PEOPLE_STORE_FILE):
    """保存人员和卡片到 JSON 文件。"""

    data = {
        "people": [],
        "cards": [],
    }

    for person in people:
        data["people"].append(person_to_dict(person))

    for card in cards:
        data["cards"].append(card_to_dict(card))

    with data_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"人员和卡片已保存到：{data_file}")


def load_people_and_cards(data_file=PEOPLE_STORE_FILE):
    """从 JSON 文件读取人员和卡片。"""

    if not data_file.exists():
        return [], []

    with data_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    people = []
    cards = []

    for person_dict in data.get("people", []):
        people.append(dict_to_person(person_dict))

    for card_dict in data.get("cards", []):
        cards.append(dict_to_card(card_dict))

    return people, cards


def build_people_summary(people, cards):
    """生成人员与卡片摘要。"""

    active_people_count = 0
    active_card_count = 0
    person_type_counts = {
        "正式工": 0,
        "三方": 0,
        "访客": 0,
    }

    for person in people:
        if person.is_active:
            active_people_count += 1

        if person.person_type in person_type_counts:
            person_type_counts[person.person_type] += 1

    for card in cards:
        if card.is_active:
            active_card_count += 1

    return {
        "total_people": len(people),
        "active_people": active_people_count,
        "total_cards": len(cards),
        "active_cards": active_card_count,
        "person_type_counts": person_type_counts,
    }


def print_people_summary(summary):
    """打印人员与卡片摘要。"""

    print(f"人员总数：{summary['total_people']}")
    print(f"启用人员数：{summary['active_people']}")
    print(f"卡片总数：{summary['total_cards']}")
    print(f"启用卡片数：{summary['active_cards']}")
    print("人员类型统计：")

    for person_type, count in summary["person_type_counts"].items():
        print(f"- {person_type}：{count}")
