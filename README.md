# Usage

#### Run PostgreSQL in Docker  
``` shell  
 docker run -d \
--name myPostgresDb \
-p 5432:5432 \
-e POSTGRES_USER=root \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_DB=suppliers \
-e POSTGRES_HOST=localhost \
postgres
```

# Useful info

#### Virtual environment (Mac OS)
``` shell
python3 -m venv venv
source venv/bin/activate
```
