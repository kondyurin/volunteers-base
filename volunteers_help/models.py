import json

from volunteers_help import db
from volunteers_help.config import basedir


def get_json(filename):
    with open (filename) as f:
        data = json.load(f)
    return data


volunteer_streets = db.Table('volunteer_streets',
                               db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteer.id')),
                               db.Column('street_id', db.Integer, db.ForeignKey('street.id')))


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    streets = db.relationship('Street', back_populates='district')

    @staticmethod
    def init_district():
        districts = get_json(f'{basedir}/volunteers_help/json/districts.json')
        streets = get_json(f'{basedir}/volunteers_help/json/streets.json')
        for k,v in districts.items():
            district = District(id=k, title=v['title'])
            db.session.add(district)
        db.session.commit()
        for k,v in districts.items():
            for k1,v1 in streets.items():
                for street_id in v['streets']:
                    if street_id == int(k1):
                        district = District.query.filter_by(id=int(k)).first()
                        street = Street(title=v1['title'], district=district)
                        db.session.add(street)
        db.session.commit()


class Street(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    district = db.relationship('District', back_populates='streets')
    volunteers = db.relationship('Volunteer', secondary='volunteer_streets', back_populates='streets')

    @staticmethod
    def init_street_volonteers():
        streets = get_json(f'{basedir}/volunteers_help/json/streets.json')
        for k, v in streets.items():
            volunteers = Volunteer.query.all()
            for volunteer in volunteers:
                for vid in v['volunteer']:
                    if vid == volunteer.id:
                        street = Street.query.filter_by(id=int(k)).first()
                        volunteer.streets.append(street)
                        db.session.add(volunteer)
        db.session.commit()


class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    userpic = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    streets = db.relationship('Street', secondary='volunteer_streets', back_populates='volunteers')

    @staticmethod
    def init_volunteer():
        volunteers = get_json(f'{basedir}/volunteers_help/json/volunteers.json')
        for k, v in volunteers.items():
            volunteer = Volunteer(id=k,
                                    name=v['name'],
                                    userpic=v['userpic'],
                                    phone=v['phone'])
            db.session.add(volunteer)
        db.session.commit()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.Integer)
    street = db.Column(db.Integer)
    volunteer = db.Column(db.Integer)
    address = db.Column(db.String(50))
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    text = db.Column(db.String(200))