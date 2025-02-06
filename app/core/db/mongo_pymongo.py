from pymongo import MongoClient
import os
from django.conf import settings

class PyMongoConnection:
    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PyMongoConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name=None):
        """pymongo 연결 정보 초기화"""
        if self._client is None:
            self._client = MongoClient(settings.MONGODB_SETTINGS['url'])
        self._db = self._client[db_name or settings.MONGODB_SETTINGS['db_name']]
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.db_name = os.getenv("MONGO_DB_NAME", "mydatabase")

    def __enter__(self):
        """with 문에서 pymongo 연결"""
        print("✅ [pymongo] MongoDB 연결 성공")
        return self  # pymongo 인스턴스를 반환하여 사용 가능

    def __exit__(self, exc_type, exc_value, traceback):
        """with 문에서 pymongo 연결 해제"""
        if self._client:
            self._client.close()
            self._client = None
            print("❌ [pymongo] MongoDB 연결 종료")

    def get_database(self):
        """데이터베이스 객체 반환"""
        return self._db

    def get_collection(self, collection_name):
        """컬렉션 객체 반환"""
        return self._db[collection_name]

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
