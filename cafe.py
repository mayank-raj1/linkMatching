import json
import random

def get_random_cafe():
    with open("data/cafes.json", 'r') as file:
        cafes = json.load(file)
    return random.choice(cafes)["cafe"]

print(get_random_cafe())