from flask import Blueprint, jsonify, request, render_template
from app import db


main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    # Fetch all documents from the 'houses' collection
    docs = db.collection('houses').stream()

    houses = []
    for doc in docs:
        houses.append(doc.to_dict())

    return jsonify(houses)

@main.route('/camera', methods=['GET'])
def camera():
    # Implement your logic here
    return jsonify({"message": "Camera endpoint"})

@main.route('/analytics', methods=['GET'])
def analytics():
    # Implement your logic here
    return jsonify({"message": "Analytics endpoint"})


@main.route('/add_house', methods=['POST'])
def add_house():
    data = request.get_json()  # get the data from the request

    # add a new document to the 'houses' collection
    doc_ref = db.collection('houses').document()
    doc_ref.set(data)

    return jsonify({"message": "House added successfully"}), 200

@main.route('/button', methods=['GET'])
def button():
    return render_template('page.html')