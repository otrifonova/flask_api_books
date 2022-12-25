def required_fields_in_data(data, required_fields):
    for field in required_fields:
        if field not in data:
            return False
    return True


def is_object_in_db(model, id):
    obj = model.query.get(id)
    return bool(obj)
