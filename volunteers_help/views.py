from flask import jsonify, request

from volunteers_help import app, db
from volunteers_help.models import District, Street, Order


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
    to_json = []
    district_id = request.args.get('district')
    streets = Street.query.filter_by(district_id=district_id).all()
    for street in streets:
        volunteers_ids = [volunteer.id for volunteer in street.volunteers]
        streets = {
            'id': street.id,
            'title': street.title,
            'volunteer': volunteers_ids
        }
        to_json.append(streets)
    return jsonify(to_json)


@app.route('/api/v1.0/volunteers/', methods=['GET'])
def get_volunteers():
    to_json = []
    street_id = request.args.get('street')
    streets = Street.query.filter_by(id=street_id).all()
    for street in streets:
        for volunteer in street.volunteers:
            volunteers = {
                'id': volunteer.id,
                'name': volunteer.name,
                'userpic': volunteer.userpic,
                'phone': volunteer.phone
            }
            to_json.append(volunteers)
    return jsonify(to_json)


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
