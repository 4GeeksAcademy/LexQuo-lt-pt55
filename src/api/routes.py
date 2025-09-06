"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import Courtfile, db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from .constants import PROVINCIAS_ARGENTINAS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# -----------------ROUTES PARA COURTFILES--------------------------------------------


@api.route('/courtfiles', methods=['GET'])
def get_courtfiles():
    try:
        courtfiles = Courtfile.query.all()
        return jsonify([courtfile.serialize() for courtfile in courtfiles]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/courtfiles/<int:courtfile_id>', methods=['GET'])
def get_courtfile(courtfile_id):
    try:
        courtfile = Courtfile.query.get_or_404(courtfile_id)
        return jsonify(courtfile.serialize()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@api.route('/courtfiles', methods=['POST'])
def create_courtfile():
    try:
        data = request.get_json()

        required_fields = ['case_number', 'title',
                           'description', 'jurisdiction', 'court', 'status']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Required field: {field}'}), 400

        existing = Courtfile.query.filter_by(
            case_number=data['case_number']).first()
        if existing:
            return jsonify({'error': 'Case number already exists'}), 409

        if data['jurisdiction'] not in PROVINCIAS_ARGENTINAS:
            return jsonify({
                'error': 'Invalid jurisdiction',
                'valid_jurisdictions': PROVINCIAS_ARGENTINAS
            }), 400

        courtfile = Courtfile(
            case_number=data['case_number'],
            title=data['title'],
            description=data['description'],
            jurisdiction=data['jurisdiction'],
            court=data['court'],
            status=data['status']
        )

        db.session.add(courtfile)
        db.session.commit()

        return jsonify(courtfile.serialize()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api.route('/courtfiles/<int:courtfile_id>', methods=['PUT'])
def update_courtfile(courtfile_id):
    try:
        courtfile = Courtfile.query.get_or_404(courtfile_id)
        data = request.get_json()

        if 'case_number' in data:
            if data['case_number'] != courtfile.case_number:
                existing = Courtfile.query.filter_by(
                    case_number=data['case_number']).first()
                if existing:
                    return jsonify({'error': 'Case number already exists'}), 409
            courtfile.case_number = data['case_number']

        if 'title' in data:
            courtfile.title = data['title']

        if 'description' in data:
            courtfile.description = data['description']

        if 'jurisdiction' in data:
            if data['jurisdiction'] not in PROVINCIAS_ARGENTINAS:
                return jsonify({
                    'error': 'Invalid jurisdiction',
                    'valid_jurisdictions': PROVINCIAS_ARGENTINAS
                }), 400
            courtfile.jurisdiction = data['jurisdiction']

        if 'court' in data:
            courtfile.court = data['court']

        if 'status' in data:
            courtfile.status = data['status']

        db.session.commit()

        return jsonify(courtfile.serialize()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api.route('/courtfiles/<int:courtfile_id>', methods=['DELETE'])
def delete_courtfile(courtfile_id):
    try:
        courtfile = Courtfile.query.get_or_404(courtfile_id)

        db.session.delete(courtfile)
        db.session.commit()

        return jsonify({'message': 'Courtfile succesfully deleted'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
