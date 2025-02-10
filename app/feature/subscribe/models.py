from mongoengine import (
    Document, StringField, DateTimeField, 
    IntField, ListField, EmbeddedDocument, 
    EmbeddedDocumentField
)
from datetime import datetime

class TagObject(EmbeddedDocument):
    id = IntField(required=True)
    name = StringField(required=True)
    media = StringField(required=True)
    related_tag = IntField(required=True)
    img = StringField(required=True)
    
class HashTagObject(EmbeddedDocument):
    id = IntField(required=True)
    name = StringField(required=True)
    media = StringField(required=True)
    img = StringField(required=True)
    
class ScrapObject(EmbeddedDocument):
    id = IntField(required=True)
    media = StringField(required=True)
    
class ReporterObject(EmbeddedDocument):
    id = IntField(required=True)
    name = StringField(required=True)
    img = StringField(required=True)

class CardLogObject(EmbeddedDocument):
    id = IntField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

class OrdersObject(EmbeddedDocument):
    id = IntField(required=True)
    name = StringField(required=True)
    related_tag = IntField()
    img = StringField(required=True)
    type = StringField(required=True)
    media = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

class CountObject(EmbeddedDocument):
    tags = IntField(required=True)
    hashtags = StringField(required=True)
    scraps = StringField(required=True)
    reporters = StringField(required=True)

class Subscribe(Document):
    h_id = StringField(required=True)
    h_id_media = IntField(required=True)
    tags = ListField(EmbeddedDocumentField(TagObject), required=True)
    hashtags = ListField(EmbeddedDocumentField(HashTagObject), required=True)
    scraps = ListField(EmbeddedDocumentField(ScrapObject), required=True)
    reporters = ListField(EmbeddedDocumentField(ReporterObject), required=True)
    cards_log = ListField(EmbeddedDocumentField(CardLogObject), required=True)
    orders = ListField(EmbeddedDocumentField(OrdersObject), required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    count = EmbeddedDocumentField(CountObject, required=True)
    
    meta = {
        'collection': 'usersubscr',
        'db_name': 'subscr_renew',
        'allow_inheritance': False
    }
    
    @classmethod
    def _get_collection_name(cls):
        return cls._meta.get('collection', 'usersubscr')
    
    @classmethod
    def _get_db_name(cls):
        return cls._meta.get('db_name', 'subscr_renew')
