# Pizzeria offers pizza-of-the-day for business lunch.
# The type of pizza-of-the-day depends on the day of week.
# Having a pizza-of-the-day simplifies ordering for customers.
# They don't have to be experts on specific types of pizza.
# Also, customers can add extra ingredients to the pizza-of-the-day.
# Write a program that will form orders from customers.
import json
import os
from datetime import datetime
from typing import List


class PizzaOfTheDay:
    def __init__(self, name: str, price: float):
        self.__name = name
        self.price = price

    def __str__(self):
        return f"{self.name} -- {self.price}"

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise ValueError("price can not be less or equal to zero")
        self.__price = value

    @property
    def name(self):
        return self.__name


class MondayPizza(PizzaOfTheDay):
    def __str__(self):
        return "Monday: " + PizzaOfTheDay.__str__(self)


class TuesdayPizza(PizzaOfTheDay):
    def __str__(self):
        return "Tuesday: " + PizzaOfTheDay.__str__(self)


class WednesdayPizza(PizzaOfTheDay):
    def __str__(self):
        return "Wednesday: " + PizzaOfTheDay.__str__(self)


class ThursdayPizza(PizzaOfTheDay):
    def __str__(self):
        return "Thursday: " + PizzaOfTheDay.__str__(self)


class FridayPizza(PizzaOfTheDay):
    def __str__(self):
        return "Friday: " + PizzaOfTheDay.__str__(self)


class SaturdayPizza(PizzaOfTheDay):
    def __str__(self):
        return "Saturday: " + PizzaOfTheDay.__str__(self)


class SundayPizza(PizzaOfTheDay):
    def __str__(self):
        return "Sunday: " + PizzaOfTheDay.__str__(self)


class Feature:
    def __init__(self, name: str, price: float):
        self.__name = name
        self.price = price

    def __str__(self):
        return f"{self.name} -- {self.price}"

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise ValueError("price can not be less or equal to zero")
        self.__price = value

    @property
    def name(self):
        return self.__name


class PizzaOfTheDayFactory:
    PIZZAS = {
        0: MondayPizza,
        1: TuesdayPizza,
        2: WednesdayPizza,
        3: ThursdayPizza,
        4: FridayPizza,
        5: SaturdayPizza,
        6: SundayPizza
    }

    def __init__(self, path: str):
        if not os.path.exists(path):
            raise ValueError("given file does not exist")

        with open(path, 'r') as f:
            self.__pizza = json.load(f)

        self.__check_pizza()

    def __check_pizza(self):
        for day in range(0, 6):
            try:
                self.__pizza[day]
            except IndexError:
                raise ValueError("lost pizza for a weekday width index " + str(day))

    def get_pizza(self):
        pizza = self.__pizza[datetime.today().weekday()]
        return self.PIZZAS[datetime.today().weekday()](list(pizza.keys())[0], list(pizza.values())[0])


class FeatureStorage:
    def __init__(self, features_path: str):
        if not os.path.exists(features_path):
            raise ValueError("given file does not exist")

        with open(features_path, 'r') as f:
            features: list = json.load(f)
            self.__features = list((Feature(list(feature.keys())[0], list(feature.values())[0]) for feature in features))

    @property
    def features(self):
        return self.__features.copy()

    def __str__(self):
        return ', '.join(map(lambda feature: feature.__str__(), self.__features))


class Order:
    def __init__(self, pizza_path: str, customer: str, address: str, features: List[Feature]):
        self.__pizza = PizzaOfTheDayFactory(pizza_path).get_pizza()
        self.customer = customer
        self.address = address
        self.features = features

    @property
    def pizza(self):
        return self.__pizza

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, value: str):
        self.__customer = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value: str):
        self.__address = value

    @property
    def features(self):
        return self.__features

    @features.setter
    def features(self, value: List[Feature]):
        self.__features = value

    @property
    def price(self):
        price = self.pizza.price
        x = (feature.price for feature in self.__features)
        return round(price + sum(x), 2)

    def features_str(self):
        if len(self.features) > 0:
            return "Features: " + ', '.join(map(lambda feature: feature.__str__(), self.features))
        return ''

    def __str__(self):
        return f"{self.customer} - {self.address}\n--> {self.pizza}\n{self.features_str()}\nTotal price: {self.price}"



