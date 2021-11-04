# Pizzeria offers pizza-of-the-day for business lunch.
# The type of pizza-of-the-day depends on the day of week.
# Having a pizza-of-the-day simplifies ordering for customers.
# They don't have to be experts on specific types of pizza.
# Also, customers can add extra ingredients to the pizza-of-the-day.
# Write a program that will form orders from customers.
import json
import os
from datetime import datetime


class PizzaOfTheDay:
    def __init__(self, name: str):
        self.__name = name

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.__name


class PizzaOfTheDayFactory:
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise ValueError("given file does not exist")

        with open(path, 'r') as f:
            self.__pizza = json.load(f)

        self.__check_pizza()

    def __check_pizza(self):
        for day in range(0, 6):
            if not str(day) in self.__pizza:
                raise ValueError("lost pizza for a weekday width index " + str(day))

    def get_pizza(self):
        return PizzaOfTheDay(self.__pizza[str(datetime.today().weekday())])


class PizzaOfTheDayWithFeatures(PizzaOfTheDay):
    def __init__(self, name: str, features=None):
        PizzaOfTheDay.__init__(self, name)

        if not features:
            features = list()
        self.features = features

    def __str__(self):
        if len(self.features) == 0:
            return PizzaOfTheDay.__str__(self)

        return f"{self.name} with additional ingredients: {', '.join(self.features)}"

    # @property
    # def features(self):
    #     return self.__features
    #
    # @features.setter
    # def features(self, features: list):
    #     self.__features = features


class PizzaOfTheDayWithFeaturesFactory(PizzaOfTheDayFactory):
    def __init__(self, pizza_path: str, features_path: str):
        PizzaOfTheDayFactory.__init__(self, pizza_path)

        if not os.path.exists(features_path):
            raise ValueError("given file does not exist")

        with open(features_path, 'r') as f:
            self.__features: list = json.load(f)

    def get_features_dict(self):
        return dict(zip(range(1, len(self.__features)), self.__features))

    def get_pizza(self):
        return PizzaOfTheDayWithFeatures(PizzaOfTheDayFactory.get_pizza(self).name)

    def check_features(self, features: list):
        for feature in features:
            if feature not in self.__features:
                raise ValueError(f"feature '{feature}' does not exist")

    def get_pizza_with_features(self, features: list):
        self.check_features(features)

        return PizzaOfTheDayWithFeatures(
            PizzaOfTheDayFactory.get_pizza(self).name,
            features
        )


class Order:
    def __init__(self, pizza: PizzaOfTheDayWithFeatures, customer: str, address: str):
        self.pizza = pizza
        self.customer = customer
        self.address = address

    @property
    def pizza(self):
        return self.__pizza

    @pizza.setter
    def pizza(self, value: PizzaOfTheDayWithFeatures):
        self.__pizza = value

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

    def __str__(self):
        return f"{self.customer} - {self.address}\n--> {self.pizza}"


