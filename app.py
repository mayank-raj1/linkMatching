from flask import Flask, request, jsonify
import random

from cafe import get_random_cafe
from introduction import introduction

app = Flask(__name__)


def get_pairs(phone_numbers):
    # replace with actual matching
    return [("123-456-7890", "234-567-8901"), ("345-678-9012", "456-789-0123")]


@app.route('/match', methods=['POST'])
def match():
    data = request.json
    phone_numbers = []
    user_info = {}

    for item in data:
        phone = item.get('Phone')
        if phone:
            phone_numbers.append(phone)
            user_info[phone] = {
                'name': item.get('Name', ''),
                'bio': item.get('Bio', ''),
                'response': item.get('Response', ''),
                'availability': item.get('Availability', '')
            }

    pairs = get_pairs(phone_numbers)
    results = []

    for phone1, phone2 in pairs:
        intro1 = introduction(**user_info[phone2])
        intro2 = introduction(**user_info[phone1])
        cafe = get_random_cafe()

        result = {
            phone1: intro1,
            phone2: intro2,
            'cafeinfo': cafe
        }
        results.append(result)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)