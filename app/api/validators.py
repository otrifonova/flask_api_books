from app.models import ModelGetter

def required_fields_in_data(data, required_fields):
    for field in required_fields:
        if field not in data:
            return False
    return True


def is_object_in_db(model, id):
    obj = model.query.get(id)
    return bool(obj)


def validate_foreign_keys(entity, data):
    response_message = []
    foreign_keys = ModelGetter.get_foreign_keys(entity)

    for fk, model in foreign_keys.items():
        if fk in data:
            id = data[fk]
            if not id:
                response_message.append(f'Field "{fk}" cannot be empty')
            elif not is_object_in_db(model, id):
                response_message.append(f"{model.get_name()} with id = {id} doesn't exist")

    return response_message
