"""A program to generate a set of abilities based on a user's name."""

from random import seed, choice, choices
import csv

# Initialise
with open("powers.csv", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    powers = list(reader)

max_rarity = max(int(power["rarity"]) for power in powers)


def calculate_luck(name):
    """Calculate a 'luck' score from 0-100 based on the user's name."""

    # Determine luck 0-100:

    # 33% weighted by balance of consonants and vowels in name

    vowels = "aeiouAEIOU"
    consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"

    vowel_count = sum(1 for char in name if char in vowels)
    consonant_count = sum(1 for char in name if char in consonants)

    if vowel_count + consonant_count == 0:
        vowel_consonant_balance = 1
    else:
        vowel_consonant_balance = 1 - (abs(vowel_count - consonant_count) / (vowel_count + consonant_count))

    # 33% weighted by balance of odd and even numbered letters in name

    odd_count = sum(1 for char in name if char.isalpha() and (ord(char.lower()) - ord('a')) % 2 == 0)
    even_count = sum(1 for char in name if char.isalpha() and (ord(char.lower()) - ord('a')) % 2 != 0)

    if odd_count + even_count == 0:
        odd_even_balance = 1
    else:
        odd_even_balance = 1 - (abs(odd_count - even_count) / (odd_count + even_count))

    # 33% weighted by length of name, luckiest is 6

    length = len(name)
    length_score = 1 - (abs(6 - length) / (6 + length))

    luck = (vowel_consonant_balance + odd_even_balance + length_score) / 3 * 100
    return int(round(luck))


def calculate_rarity_weights(luck, constant):
    """Calculate weights for each rarity level based on luck and a constant."""
    weights = []
    for rarity in range(1, max_rarity + 1):
        weight = (rarity**luck) / (constant**rarity)
        weights.append(weight)
    return weights


def generate_power_ids():
    """Generate a list of power IDs based on the ability rarities."""
    powers_copy = powers.copy()
    power_ids = []
    for rarity in ability_rarities:
        if len([power for power in powers_copy if power["rarity"] == str(rarity)]) == 0:
            continue # no powers of this rarity left - hopefully this wont happen as the table gets larger
        power_id = choice([power["ID"] for power in powers_copy if power["rarity"] == str(rarity)])
        power_ids.append(power_id)
        powers_copy.remove(next(power for power in powers_copy if power["ID"] == power_id)) # prevent duplicate powers
    return power_ids


def display_available_powers():
    """Display all available powers based on the ability rarities."""
    print("You can have the following powers:")
    for power in powers:
        if power["rarity"] in [str(rarity) for rarity in ability_rarities]:
            print(f"{power["name"]} [LV.{power["rarity"]}]")


def display_powers(power_ids):
    """Display the generated powers based on their IDs.
    
    Args:
        power_ids (list): A list of power IDs to display.
    """
    print("You have the following powers:")
    for power_id in power_ids:
        power = [power for power in powers if power["ID"] == power_id][0]
        print(f"> {power['name']} [LV.{power['rarity']}] - {power['description']}")


name = input("Enter your name: ")
print(f"Hello, {name}!")

luck = calculate_luck(name)
luck_modified = luck**2 / 400 # for calculating rarity weights
luck_modified_2 = luck**2 / 2000 # for calculating number of abilties
print(f"Your luck score is: {luck}\n")

luck_affected_rarities = calculate_rarity_weights(luck_modified, 32)
total_weight = sum(luck_affected_rarities)
normalised_rarities = [weight / total_weight for weight in luck_affected_rarities]

luck_affected_abilities = calculate_rarity_weights(luck_modified_2, 4)
total_weight_abilities = sum(luck_affected_abilities)
normalised_abilities = [weight / total_weight_abilities for weight in luck_affected_abilities]

seed(sum([ord(c.lower()) for c in name]))
# seed is sum of ascii values of name in lowercase: e.g. "Mike" = 109+105+107+101 = 422

number_of_abilities = choices(
    population=list(range(1, max_rarity + 1)),
    weights=normalised_abilities
    )[0]
ability_rarities = choices(
    population=list(range(1, max_rarity + 1)),
    weights=normalised_rarities,
    k=number_of_abilities
    )
ability_rarities.sort(reverse=True) # Highest rarity abilities first


user_powers = generate_power_ids()

# Uncomment the next line to see powers available for the generated rarities
#display_available_powers()

display_powers(user_powers)
