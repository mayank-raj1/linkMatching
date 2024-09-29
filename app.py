from flask import Flask, request, jsonify
import random

from cafe import get_random_cafe
from introduction import introduction
from match import predictPair

app = Flask(__name__)


def get_pairs(phone_numbers):

    # replace with actual matching
    return [("+16478973143", "+14164276719")]


@app.route('/match', methods=['POST'])
def match():
    data = request.json
    people = []
    user_info = {}

    for item in data:
        phone = item.get('Phone')
        if phone:
            people.append(phone)
            user_info[phone] = {
                'name': item.get('Name', ''),
                'bio': item.get('Bio', ''),
                'response': item.get('Response', ''),
                'availability': item.get('Availability', '')
            }

    pairs = predictPair(data)
    results = []
    print(type(pairs))
    for index in range(0, len(pairs)):
        intro1 = introduction(**user_info[pairs[index][1]])
        intro2 = introduction(**user_info[pairs[index][0]])
        cafe = get_random_cafe()

        result = {
            pairs[index][0]: intro1,
            pairs[index][1]: intro2,
            'cafeinfo': cafe
        }
        results.append(result)

    return jsonify(results)

@app.route('/', methods=['GET'])
def testfun():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)