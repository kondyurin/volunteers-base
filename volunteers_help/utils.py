from flask import jsonify


def get_paginated_list(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        return jsonify(), 404
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + f'?start={start_copy}&limit={limit_copy}'
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + f'?start={start_copy}&limit={limit}'
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj


def get_streets_json(streets):
    to_json = []
    for street in streets:
        ids = [volunteer.id for volunteer in street.volunteers]
        street = {
            'id': street.id,
            'title': street.title,
            'volunteer': ids
        }
        to_json.append(street)
    return to_json


def get_volunteers_json(volunteers):
    to_json = []
    for volunteer in volunteers:
        volunteer = {
            'id': volunteer.id,
            'name': volunteer.name,
            'userpic': volunteer.userpic,
            'phone': volunteer.phone
        }
        to_json.append(volunteer)
    return to_json
