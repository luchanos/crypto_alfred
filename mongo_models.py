from mongoengine import BooleanField, Document, IntField, StringField


class User(Document):
    user_id = IntField(required=True, unique=True)
    status = StringField(default="Mr. Andersen")
    accepted_rules = BooleanField(default=False)
    chat_id = StringField(required=True, unique=True)
    referral_link = StringField(unique=True, sparse=True)
    level = StringField()
    rating = IntField(default=0)
    is_deleted = BooleanField(default=False)
