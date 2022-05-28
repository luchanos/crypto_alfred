from mongoengine import StringField, IntField, BooleanField, connect, Document


class User(Document):
    user_id = IntField(required=True)
    status = StringField(default="Mr. Andersen")
    accepted_rules = BooleanField(default=False)
    chat_id = StringField(required=True)
    referal_link = StringField(default=None)
    level = StringField(required=None)
