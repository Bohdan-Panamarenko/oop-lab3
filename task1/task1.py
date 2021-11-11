# Write a program for selling tickets to IT-events. Each ticket has a unique number and a price.
# There are four types of tickets: regular ticket, advance ticket (purchased 60 or more days before
# the event), late ticket (purchased fewer than 10 days before the event) and student ticket.
# Additional information:
# -advance ticket - discount 40% of the regular ticket price;
# -student ticket - discount 50% of the regular ticket price;
# -late ticket - additional 10% to the regular ticket price.
# All tickets must have the following properties:
# -the ability to construct a ticket by number;
# -the ability to ask for a ticket’s price;
# -the ability to print a ticket as a String.
from datetime import datetime, timedelta
import json
import os
from uuid import uuid4


class RegularTicket:
    def __init__(self, seat: int, name: str, description: str, price: float, date: datetime):
        self.__name = name
        self.__seat = seat
        self.__description = description
        self.__price = price
        self.__date = date
        self.__uuid = uuid4()

    @property
    def price(self):
        return self.__price

    def __str__(self):
        return f"{self.__class__.__name__} -- {self.__uuid}\n" \
               f"'{self.__name}': seat {self.__seat}, date {self.__date.date()}\n" \
               f"{self.__description}\n" \
               f"Price {self.price}"

    def __get_dict(self):
        obj = dict()
        obj["name"] = self.__name
        obj["seat"] = self.__seat
        obj["description"] = self.__description
        obj["price"] = self.__price
        obj["date"] = self.__date.date().__str__()
        obj["uuid"] = self.__uuid.__str__()
        return obj

    def serialize(self):
        with open(f'tickets/{self.__class__.__name__}-{self.__uuid}.json', 'w', encoding='utf-8') as f:
            json.dump(self.__get_dict(), f, ensure_ascii=False, indent=2)


class AdvancedTicket(RegularTicket):
    def __init__(self, seat: int, name: str, description: str, price: float, date: datetime):
        RegularTicket.__init__(self, seat, name, description, round(price * 0.6, 2), date)


class StudentTicket(RegularTicket):
    def __init__(self, seat: int, name: str, description: str, price: float, date: datetime):
        RegularTicket.__init__(self, seat, name, description, round(price * 0.5, 2), date)


class LateTicket(RegularTicket):
    def __init__(self, seat: int, name: str, description: str, price: float, date: datetime):
        RegularTicket.__init__(self, seat, name, description, round(price * 1.1, 2), date)


class TicketPattern:
    def __init__(self, ticket_pattern: dict):
        try:
            self.__set_name(ticket_pattern["name"])
            self.__set_description(ticket_pattern["description"])
            self.__set_price(ticket_pattern["price"])
            self.__set_seats(ticket_pattern["seats"])
            self.__set_date(ticket_pattern["date"])
        except KeyError as e:
            raise ValueError("lost necessary field: " + e.__str__())

    def __set_name(self, value: str):
        if value == "":
            raise ValueError("name can not be empty")
        self.__name = value

    def __set_description(self, value: str):
        if value == "":
            raise ValueError("name can not be empty")
        self.__description = value

    def __set_price(self, value: float):
        if value <= 0:
            raise ValueError("price can not be less or equal to zero")
        self.__price = value

    def __set_seats(self, value: int):
        if value <= 0:
            raise ValueError("seats number can not be less or equal to zero")
        self.__seats = value

    def __set_date(self, value: str):
        self.__date = datetime.strptime(value, "%y-%m-%d")

    def get_ticket(self, seat: int) -> RegularTicket:
        time_to_concert = self.date - datetime.today()

        if time_to_concert >= timedelta(days=60):
            return AdvancedTicket(seat, self.name, self.description, self.price, self.date)

        elif timedelta(days=10) > time_to_concert:
            return LateTicket(seat, self.name, self.description, self.price, self.date)

        else:
            return RegularTicket(seat, self.name, self.description, self.price, self.date)

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def price(self):
        return self.__price

    @property
    def seats(self):
        return self.__seats

    @property
    def date(self):
        return self.__date

    def __str__(self):
        return self.get_ticket(0).__str__() + f"\nRegular price {self.price}"


class TicketFactory:
    def __init__(self, ticket_pattern: dict):
        self.__tp = TicketPattern(ticket_pattern)
        self.__sold = dict()

    @property
    def name(self):
        return self.__tp.name

    @property
    def description(self):
        return self.__tp.description

    @property
    def price(self):
        return self.__tp.price

    @property
    def seats(self):
        return self.__tp.seats

    @property
    def date(self):
        return self.__tp.date

    def __mark(self, seat: int):
        if seat not in self.__sold and self.seats >= seat > 0:
            self.__sold[seat] = True
        else:
            raise ValueError(f"seat with number '{seat}' is already taken or invalid, try to get another seat")

    def free_seats(self) -> set:
        all_seats = set(range(1, self.seats))
        return all_seats - set(self.__sold.keys())

    def get_ticket(self, seat: int) -> RegularTicket:
        time_to_concert = self.date - datetime.today()
        if time_to_concert < timedelta(0):
            raise RuntimeError("this concert is already gone")

        self.__mark(seat)
        return self.__tp.get_ticket(seat)

    def get_student_ticket(self, seat: int) -> RegularTicket:
        time_to_concert = self.date - datetime.today()
        if time_to_concert < timedelta(0):
            raise RuntimeError("this concert is already gone")

        self.__mark(seat)
        return StudentTicket(seat, self.name, self.description, self.price, self.date)

    def __str__(self):
        return self.__tp.__str__()


class TicketsStore:
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise ValueError("given file does not exist")

        with open(path, 'r') as f:
            tickets = json.load(f)

            self.__t_facts = dict()

            i = 1
            for tkt in tickets:
                self.__t_facts[i] = TicketFactory(tkt)
                i += 1

    def list(self):
        return list(map(lambda key: f"{key}) {self.__t_facts[key].__str__()}", self.__t_facts.keys()))

    def get_factory(self, number: int):
        tf = self.__t_facts.get(number, None)
        if not tf:
            raise LookupError("ticket factory with such number does not exist")

        return tf

    def buy(self, tf_num: int, seat_num):
        tf = self.get_factory(tf_num)

        return tf.get_ticket(seat_num)

    def buy_student(self, tf_num: int, seat_num):
        tf = self.get_factory(tf_num)

        return tf.get_student_ticket(seat_num)



