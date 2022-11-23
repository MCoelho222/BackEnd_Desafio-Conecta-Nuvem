def create_collection_contacts(mongo_client):
    contacts_validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'title': 'Validação de usuário',
            'required': [
                'email',
            ],
            'properties': {
                'email': {
                'bsonType': "string"
                },
            },
        }
    }
    try:
        mongo_client.create_collection('contacts')
    except Exception as e:
        print(e)
        return {"error": "Collection exists."}
    
    mongo_client.command('collMod', 'contacts', validator=contacts_validator)