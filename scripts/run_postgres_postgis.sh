docker pull postgis/postgis:16-3.4-alpine
docker run --rm -P -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD="postgres_pw" -e POSTGRES_USER="test_user" -d --name flask_postgres postgis/postgis:16-3.4-alpine
echo SQLALCHEMY_DATABASE_URI=postgresql://test_user:postgres_pw@127.0.0.1:5432/postgres >> .env