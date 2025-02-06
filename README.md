# django를 사용한 웹 프로젝트

## 기술 스택

- Python 3.13
- Django 4.2.1
- Docker 24.0.1
- Docker Compose 2.19.1

## 프로젝트 구조
- app/core : 공통 기능 구현
- app/feature : 기능 구현
- manage.py : 프로젝트 실행
- nginx : 웹 서버 구현
- docker-compose.yml : 프로젝트 실행
- docker : 도커파일
- requirements.txt : 기능 구현

## 시작

```bash
docker-compose build --no-cache django-dev # 개발 환경 빌드
docker compose up -d # 개발 환경 실행
```
