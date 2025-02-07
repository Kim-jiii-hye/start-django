from mongoengine import connect, disconnect
from mongoengine.connection import get_connection
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
from app.feature.subscribe.models import Subscribe  # Subscribe 모델 import

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
        
        self.mongo_uri = os.environ.get('MONGO_URI')
        if not self.mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set")
            
        if db_name is None:
            self.db_name = os.environ.get('MONGO_DB_SUBSCRIBE')
            if not self.db_name:
                raise ValueError("MONGO_DB_SUBSCRIBE environment variable is not set")
        else:
            self.db_name = db_name
        # models.py의 메타 정보에서 컬렉션 이름 가져오기
        self.collection = collection or Subscribe._meta.get('collection', 'usersubscr')
        logger.info(f"🔄 MongoDB Settings - DB: {self.db_name}, Collection: {self.collection}")

    def __enter__(self):
        """with 문에서 mongoengine 연결"""
        try:
            if not self.db_name:
                raise ValueError("Database name cannot be empty")
                
            # db_alias를 models.py의 메타 정보와 일치시킴
            connect(db=self.db_name, host=self.mongo_uri, 
                   alias=Subscribe._meta.get('db_alias', 'default'),
                   serverSelectionTimeoutMS=5000)
            
            # 연결 테스트
            conn = get_connection()
            db = conn.get_database(self.db_name)
            print(f"✅ [mongoengine] MongoDB 연결 성공")
            return self
        except Exception as e:
            print(f"❌ [mongoengine] MongoDB 연결 실패: {str(e)}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        """with 문에서 mongoengine 연결 해제"""
        try:
            disconnect()
            print("✅ [mongoengine] MongoDB 연결 종료")
        except Exception as e:
            print(f"❌ [mongoengine] MongoDB 연결 해제 실패: {str(e)}")
