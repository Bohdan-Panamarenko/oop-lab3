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


actions = {
    1: buy_ticket,
    2: list_bought_tickets,
    3: list_free_seats,
    4: exit
}


ts = TicketsStore("../ticket.json")
tickets = list()

print(f"Today is: {datetime.today().date()}")
print("List of tickets for sale:")
print("\n----------\n".join(ts.list()))

while True:
    print("\nAllowed actions:")
    print("--> 1. Buy ticket")
    print("--> 2. List bought tickets")
    print("--> 3. List free seats")
    print("--> 4. Exit")

    val = input("Choose an action: ")

    num: int

    try:
        num = int(val)
    except Exception as e:
        print_err(e)
        continue

    if not 1 <= num <= 4:
        print("Expected int in range from 1 to 4")

    actions[num]()

