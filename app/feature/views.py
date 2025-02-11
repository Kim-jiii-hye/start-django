from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='get',
    operation_description="GET 메서드 설명",
    responses={200: 'Success response'}
)
@api_view(['GET'])
def hello_world(request):
    return Response({
        "message": f"Hello, World! django",
        "status": "success"
    })