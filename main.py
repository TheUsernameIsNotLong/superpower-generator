from random import seed, choice, choices
import csv

name = input("Enter your name: ")
print(f"Hello, {name}!")

# Order:
# 1. Determine luck 0-100:
# 33% weighted by balance of consonants and vowels in name
# 33% weighted by balance of odd and even numbered letters in name
# 33% weighted by length of name, luckiest is 6

def calculate_luck(name):
    vowels = "aeiouAEIOU"
    consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
    
    vowel_count = sum(1 for char in name if char in vowels)
    consonant_count = sum(1 for char in name if char in consonants)
    
    if vowel_count + consonant_count == 0:
        vowel_consonant_balance = 1
    else:
        vowel_consonant_balance = 1 - (abs(vowel_count - consonant_count) / (vowel_count + consonant_count))
    
    odd_count = sum(1 for char in name if char.isalpha() and (ord(char.lower()) - ord('a')) % 2 == 0)
    even_count = sum(1 for char in name if char.isalpha() and (ord(char.lower()) - ord('a')) % 2 != 0)
    
    if odd_count + even_count == 0:
        odd_even_balance = 1
    else:
        odd_even_balance = 1 - (abs(odd_count - even_count) / (odd_count + even_count))
    
    length = len(name)
    length_score = 1 - (abs(6 - length) / (6 + length))
    
    luck = (vowel_consonant_balance + odd_even_balance + length_score) / 3 * 100
    return int(round(luck))

def sigma(array, start=0, end=0):
    if start < 0 or start > len(array) - 1:
        start = 0
    if end - start < 1:
        end = len(array)
    sum_n = 0
    for n in range(start, end):
        sum_n += array[n]
    return sum_n

luck = calculate_luck(name)
luck_modified = luck**2 / 400 # for calculating rarity weights
luck_modified_2 = luck**2 / 2000 # for calculating number of abilties
print(f"Your luck score is: {luck}")
print(sigma([2**i for i in range(-1, -10, -1)]))

def calculate_rarity_weights(luck, constant):
    weights = []
    for rarity in range(1, 11):
        weight = (rarity**luck) / (constant**rarity)
        weights.append(weight)
        print(weight)
    return weights

luck_affected_rarities = calculate_rarity_weights(luck_modified, 32)
total_weight = sigma(luck_affected_rarities)
normalised_rarities = [weight / total_weight for weight in luck_affected_rarities]
print(normalised_rarities)

luck_affected_abilities = calculate_rarity_weights(luck_modified_2, 4)
total_weight_abilities = sigma(luck_affected_abilities)
normalised_abilities = [weight / total_weight_abilities for weight in luck_affected_abilities]


seed(sum([ord(c.lower()) for c in name])+1) # seed is sum of ascii values of name in lowercase, plus 1: e.g. "Mike" = 109+105+107+101+1 = 423
# plus 1 because the name "mike" leads to somehow rolling a single ability of rarity 1, which im not a fan of for unbiased reasons i wont bore you with.

number_of_abilities = choices(population=[i for i in range(1, 11)],weights=normalised_abilities)[0]
ability_rarities = choices(population=[i for i in range(1, 11)], weights=normalised_rarities, k=number_of_abilities)
ability_rarities.sort(reverse=True) # Highest rarity abilities first
print(ability_rarities)

with open("powers.csv", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    powers = list(reader)

print("You can have the following powers:")
for power in powers:
    if power["rarity"] in [str(rarity) for rarity in ability_rarities]:
        print(f"{power["name"]} ({power["rarity"]})")

powersCopy = powers.copy()
powerIDs = []
for rarity in ability_rarities:
    if len([power for power in powersCopy if power["rarity"] == str(rarity)]) == 0:
        continue
    powerID = choice([power["ID"] for power in powersCopy if power["rarity"] == str(rarity)])
    powerIDs.append(powerID)
    powersCopy.remove(next(power for power in powersCopy if power["ID"] == powerID)) # prevent duplicate powers

print("You have the following powers:")
for powerID in powerIDs:
    power = [power for power in powers if power["ID"] == powerID][0]
    print(f"> {power['name']} [LV.{power['rarity']}] - {power['description']}")