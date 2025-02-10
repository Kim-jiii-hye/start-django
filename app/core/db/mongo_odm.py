from mongoengine import connect, disconnect
from mongoengine.connection import get_connection
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
import django

# Django 설정 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.feature.settings')
django.setup()

# Django settings import
from django.conf import settings

# 로거 설정
logger = logging.getLogger(__name__)

def get_app_env_path() -> Path:
    """프로젝트 루트의 .env.development 파일 경로를 반환"""
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent.parent
    env_path = project_root / '.env.development'
    
    logger.info(f"Looking for .env.development in: {project_root}")
    if not env_path.exists():
        raise FileNotFoundError(f".env.development not found in project root: {env_path}")
    
    return env_path

class MongoEngineConnection:
    def __init__(self, db_name=None, collection=None):
        """MongoEngine (ODM) 연결 정보 초기화
        Args:
            db_name (str, optional): 사용할 데이터베이스 이름
            collection (str, optional): 사용할 컬렉션 이름
        """
        env_path = get_app_env_path()
        load_dotenv(env_path)
        logger.info(f"Loaded environment from: {env_path}")
        
        # settings에서 MongoDB 설정 가져오기
        self.mongo_uri = settings.MONGODB_SETTINGS['url']
        if not self.mongo_uri:
            raise ValueError("MONGO_URI is not configured in settings")
            
        if db_name is None:
            self.db_name = settings.MONGODB_SETTINGS['subscribe']['db_name']
            if not self.db_name:
                raise ValueError("Database name is not configured in settings")
        else:
            self.db_name = db_name
        # models.py의 메타 정보에서 컬렉션 이름 가져오기
        self.collection = collection
        logger.info(f"🔄 MongoDB Settings - DB: {self.db_name}, Collection: {self.collection}")

    def __enter__(self):
        """with 문에서 mongoengine 연결"""
        try:
            if not self.db_name:
                raise ValueError("Database name cannot be empty")
            
            logger.info(f"Attempting to connect to MongoDB: {self.mongo_uri}")
            connect(db=self.db_name, host=self.mongo_uri, 
                   serverSelectionTimeoutMS=5000)

            # 연결 테스트
            conn = get_connection(self.db_name)
            db = conn.get_database(self.db_name)
            logger.info(f"✅ MongoDB 연결 성공 - DB: {self.db_name}, Collection: {self.collection}")
            return self
        except Exception as e:
            logger.error(f"❌ MongoDB 연결 실패:")
            logger.error(f"  - URI: {self.mongo_uri}")
            logger.error(f"  - DB: {self.db_name}")
            logger.error(f"  - Collection: {self.collection}")
            logger.error(f"  - Error: {str(e)}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        """with 문에서 mongoengine 연결 해제"""
        try:
            disconnect()
            print("✅ [mongoengine] MongoDB 연결 종료")
        except Exception as e:
            print(f"❌ [mongoengine] MongoDB 연결 해제 실패: {str(e)}")
