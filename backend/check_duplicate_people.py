from person_json_safe import load_people


# def check_duplicates(people):
#     seen_employee_nos = set()
#     seen_card_nos = set()

#     for person in people:
#         employee_no = person["employee_no"].upper()
#         card_no = person["card_no"].upper()

#         if employee_no in seen_employee_nos:
#             print("发现重复工号：", employee_no)

#         if card_no in seen_card_nos:
#             print("发现重复卡号：", card_no)

#         seen_employee_nos.add(employee_no)
#         seen_card_nos.add(card_no)
def check_duplicates(people):
    seen_employee_nos = {}
    seen_card_nos = {}

    for person in people:
        employee_no = person["employee_no"].upper()
        card_no = person["card_no"].upper()

        if employee_no in seen_employee_nos:
            first_person = seen_employee_nos[employee_no]
            print("发现重复工号：", employee_no)
            print("第一次出现：", first_person["name"])
            print("重复人员：", person["name"])
        else:
            seen_employee_nos[employee_no] = person

        if card_no in seen_card_nos:
            first_person = seen_card_nos[card_no]
            print("发现重复卡号：", card_no)
            print("第一次出现：", first_person["name"])
            print("重复人员：", person["name"])
        else:
            seen_card_nos[card_no] = person

def main():
    people = load_people()
    check_duplicates(people)


if __name__ == "__main__":
    main()