from mongoengine import StringField, IntField, BooleanField, Document


class User(Document):
    user_id = IntField(required=True, unique=True)
    status = StringField(default="Mr. Andersen")
    accepted_rules = BooleanField(default=False)
    chat_id = StringField(required=True, unique=True)
    referal_link = StringField(default=None, unique=True)
    level = StringField(required=None)
    rating = IntField(default=0)
