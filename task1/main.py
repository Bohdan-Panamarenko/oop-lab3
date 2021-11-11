from datetime import datetime

from task1 import TicketsStore


def print_err(err: Exception):
    print(f"Error: {err}")


def buy_ticket():
    val = input("Enter num of ticket:")

    tf_num: int

    try:
        tf_num = int(val)
    except Exception as e:
        print_err(e)
        return

    val = input("Enter num of seat:")

    seat_num: int

    try:
        seat_num = int(val)
    except Exception as e:
        print_err(e)
        return

    val = input("Are you student (1 - true, other - false):")

    is_student: int

    try:
        is_student = int(val)

        if is_student == 1:
            tickets.append(ts.buy_student(tf_num, seat_num))
        else:
            tickets.append(ts.buy(tf_num, seat_num))
    except Exception as e:
        print_err(e)
        return


def list_free_seats():
    val = input("Enter num of ticket:")

    tf_num: int

    try:
        tf_num = int(val)
        ft = ts.get_factory(tf_num)
    except Exception as e:
        print_err(e)
        return

    for seat in ft.free_seats():
        print(seat)


def list_bought_tickets():
    print("List of bought tickets:")
    print("\n----------\n".join(list(map(lambda ticket: ticket.__str__(), tickets))))


def serialize_ticket():
    if len(tickets) == 0:
        raise ValueError("You do not have any ticket yet")

    print("List of bought tickets:")
    print("\n----------\n".join(list(map(lambda index: f"--> {index}. {tickets[index].__str__()}", range(len(tickets))))))
    print("\n----------\n")

    val = input("Enter index of ticket:")

    num: int

    try:
        num = int(val)
        tickets[num].serialize()
    except Exception as e:
        print_err(e)
        return

    print("Successfully serialized!")


actions = {
    1: buy_ticket,
    2: list_bought_tickets,
    3: list_free_seats,
    4: serialize_ticket,
    5: exit
}


ts = TicketsStore("ticket.json")
tickets = list()

print(f"Today is: {datetime.today().date()}")
print("List of tickets for sale (id and seat number will be different):")
print("\n----------\n".join(ts.list()))

while True:
    print("\nAllowed actions:")
    print("--> 1. Buy ticket")
    print("--> 2. List bought tickets")
    print("--> 3. List free seats")
    print("--> 4. Serialize your ticket")
    print("--> 5. Exit")

    val = input("Choose an action: ")

    num: int

    try:
        num = int(val)
    except Exception as e:
        print_err(e)
        continue

    if not 1 <= num <= len(actions):
        print("Expected int in range from 1 to " + len(actions).__str__())

    actions[num]()

