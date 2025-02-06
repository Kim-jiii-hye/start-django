from mongoengine import connect, disconnect
import os

class MongoEngineConnection:
    def __init__(self):
        """MongoEngine (ODM) 연결 정보 초기화"""
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.db_name = os.getenv("MONGO_DB_NAME", "mydatabase")

    def __enter__(self):
        """with 문에서 mongoengine 연결"""
        connect(self.db_name, host=self.mongo_uri)
        print("✅ [mongoengine] MongoDB 연결 성공")
        return self  # mongoengine 인스턴스를 반환

    def __exit__(self, exc_type, exc_value, traceback):
        """with 문에서 mongoengine 연결 해제"""
        disconnect()
        print("❌ [mongoengine] MongoDB 연결 종료")
