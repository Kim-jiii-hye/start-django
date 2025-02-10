from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from app.core.db.mongo_odm import MongoEngineConnection
from .models import Subscribe  # Subscribe 모델 import
import json
from bson import json_util
import logging

logger = logging.getLogger(__name__)

class SubscribeViewSet(viewsets.ViewSet):
    def list(self, request):
        with MongoEngineConnection(db_name='subscr_renew'):
            subscribes = Subscribe.objects.filter(
                h_id='zxc0585',
                h_id_media=6
            ).all()
            
            subscribes_json = json.loads(
                json_util.dumps(
                    [sub.to_mongo().to_dict() for sub in subscribes]
                )
            )
            
            return Response({
                'status': 'success',
                'data': subscribes_json
            })

    @action(detail=False, methods=['post'])
    def list_by_params(self, request):
        try:
            body = json.loads(request.body)
            
            h_id = body.get('h_id')
            h_id_media = body.get('h_id_media')
            
            if not h_id or h_id_media is None:
                return Response({
                    'status': 'error',
                    'message': 'h_id and h_id_media are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                h_id_media = int(h_id_media)
            except (TypeError, ValueError):
                return Response({
                    'status': 'error',
                    'message': 'h_id_media must be a number'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"🔍 Querying with params - h_id: {h_id}, h_id_media: {h_id_media}")
            
            # 메타 정보 가져오기
            collection_name = Subscribe._get_collection_name()
            db_alias = Subscribe._get_db_name()
            
            print(f"Using collection: {collection_name}, db_alias: {db_alias}")  # 디버깅용 로그 추가
            
            with MongoEngineConnection(db_name=db_alias, collection=collection_name):
                query = Subscribe.objects.filter(
                    h_id=h_id,
                    h_id_media=h_id_media
                )
                
                subscribes = query.all()
                
                print(f"🔍 DB: {db_alias}")
                print(f"🔍 Collection: {collection_name}")
                print(f"🔍 MongoDB Query: {query._query}")
                print(f"📊 Found {subscribes} documents")
                print(f"📊 Found {subscribes.count()} documents")
                
                subscribes_json = json.loads(
                    json_util.dumps(
                        [sub.to_mongo().to_dict() for sub in subscribes]
                    )
                )
                
                return Response({
                    'status': 'success',
                    'data': subscribes_json
                })
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'Invalid JSON format'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
