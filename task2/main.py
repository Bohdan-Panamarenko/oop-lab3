import re

from task2 import FeatureStorage, Order


def print_err(err: Exception):
    print(f"Error: {err}")


def add_features(all_features: list):
    print("<-- Adding features -->")
    chosen_features = list()

    all_features_dict = dict()
    for i in range(1, len(all_features) + 1):
        all_features_dict[i] = all_features[i - 1]

    allowed_features = 3
    while allowed_features > 0:
        print("\n".join(list(map(lambda key: f"--> {key}. {all_features_dict[key]}", all_features_dict.keys()))))
        print("--> 0. End")
        val = input(f"Choose feature ({allowed_features} left):")

        num: int

        try:
            num = int(val)

            if num == 0:
                break

            chosen_features.append(all_features_dict[num])
            del(all_features_dict[num])

            allowed_features -= 1
        except Exception as e:
            print_err(e)
            continue

    print("You chose: " + ", ".join(list(map(lambda feature: feature.__str__(), chosen_features))))
    val = input("Made a mistake, try again (y - yes): ")
    if len(val) > 0 and val[0] == 'y':
        return add_features(all_features)

    return chosen_features


def continue_order(order: Order):
    while True:
        val = input("Enter your name: ")

        if re.match("[^a-zA-Z\\s]", val) or val == "":
            print_err(Exception("Name can contain only letters or spaces and can not be empty"))
            continue

        order.customer = val
        break

    while True:
        val = input("Enter your address: ")

        if val == "":
            print_err(Exception("Address can no be empty"))
            continue

        order.address = val
        break

    print("Order: " + order.__str__())
    val = input("Make order (y - yes): ")

    if len(val) > 0 and val[0] == 'y':
        print("Thank you for your order :)")
        exit(0)


def main():
    fs = FeatureStorage("features.json")
    order = Order("pizza.json", "", "", [])

    print(f"Today we are having: {order.pizza}")
    print("You can add some additional ingredients to your pizza!")
    print(f'There are:\n{ fs.__str__() }')

    while True:
        print(f"\nOrder for now: " + order.__str__() + "\n")
        print("Allowed actions:")
        print("--> 1. Add features")
        print("--> 2. Continue ordering")
        print("--> 3. Exit")
        val = input("Choose action:")

        num: int

        try:
            num = int(val)
        except Exception as e:
            print_err(e)
            exit(0)
            continue

        if num == 1:
            order.features = add_features(fs.features)
        elif num == 2:
            continue_order(order)
        else:
            exit(0)


main()




