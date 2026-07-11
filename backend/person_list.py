people = [
    {
        "name": "张伟",
        "employee_no": "BBAC10001",
        "card_no": "0012345678",
        "person_type": "正式工",
        "is_active": True,
    },
    {
        "name": "李娜",
        "employee_no": "BBAC10002",
        "card_no": "0012345679",
        "person_type": "实习生",
        "is_active": False,
    }
]



# print(person)
# print(person["name"])
# print(person["card_no"])
for person in people:
    print(
        f"姓名：{person['name']}，"
        f"工号：{person['employee_no']}，"
        f"卡号：{person['card_no']}"
    )

print(f"人员列表：{len(people)}人")
new_person = {
    "name": input("请输入姓名：").strip(),
    "employee_no": input("请输入工号：").strip(),
    "card_no": input("请输入NFC卡号：").strip(),
    "person_type": input("请输入人员类型：").strip(),
    "is_active": True,
}

people.append(new_person)