from flask import jsonify, request

from volunteers_help import app, db
from volunteers_help.utils import get_paginated_list, \
                                  get_streets_json, \
                                  get_volunteers_json
from volunteers_help.models import District, Street, Order, Volunteer


@app.route('/api/v1.0/districts/', methods=['GET'])
def get_districts():
    to_json = []
    districts = District.query.all()
    for district in districts:
        districts = {
            'id': district.id,
            'title': district.title
        }
        to_json.append(districts)
    return jsonify(to_json)


@app.route('/api/v1.0/streets/', methods=['GET'])
def get_streets():
    district_id = request.args.get('district')
    if not district_id:
        streets = Street.query.all()
        to_json = get_streets_json(streets)
        return jsonify(get_paginated_list(
                       to_json,
                       '/api/v1.0/streets/',
                       start=request.args.get('start', 1),
                       limit=request.args.get('limit', 10)
                       ))
    streets = Street.query.filter_by(district_id=district_id).all()
    to_json = get_streets_json(streets)
    return jsonify(get_paginated_list(
                   to_json,
                   f'/api/v1.0/streets/?district={district_id}&',
                   start=request.args.get('start', 1),
                   limit=request.args.get('limit', 10)
                   ))


@app.route('/api/v1.0/volunteers/', methods=['GET'])
def get_volunteers():
    to_json = []
    street_id = request.args.get('street')
    if not street_id:
        volunteers = Volunteer.query.all()
        to_json = get_volunteers_json(volunteers)
        return jsonify(get_paginated_list(
                   to_json,
                   '/api/v1.0/volunteers/',
                   start=request.args.get('start', 1),
                   limit=request.args.get('limit', 10)
                   ))
    street = Street.query.filter_by(id=street_id).first()
    volunteers = street.volunteers
    to_json = get_volunteers_json(volunteers)
    return jsonify(get_paginated_list(
                   to_json,
                   f'/api/v1.0/volunteers/?street={street_id}&',
                   start=request.args.get('start', 1),
                   limit=request.args.get('limit', 10)
                   ))


@app.route('/helpme/', methods=['POST'])
def order():
    data = request.json
    if not data:
        return jsonify(), 400
    order = Order(district=data.get('district'),
                  street=data.get('street'),
                  volunteer=data.get('volunteer'),
                  address=data.get('address'),
                  name=data.get('name'),
                  surname=data.get('surname'),
                  phone=data.get('phone'),
                  text=data.get('text'))
    db.session.add(order)
    db.session.commit()
    return jsonify({'status': 'success'}), 201, \
        {'Location': f'/helpme/{order.id}/'}
