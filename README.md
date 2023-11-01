# DAI

## IMPORTANTE

Para lo esté en requirements.txt
- docker compose build 

Ejecuta " ython manage.py runserver 0.0.0.0:8000"
- docker compose up 


## Practica 1


## Practica 2
Metemos en los requerimientos 'django==4.2' y en el .yml:
    ports:
      - 8000:8000
    depends_on:
      - mongo
    command: python manage.py runserver 0.0.0.0:8000

iniciamos la app
docker compose run --rm app django-admin startproject Ecommerce .

- iniciamos el migrate para crear la bd para users
docker compose run app python manage.py migrate

- iniciamos el server

docker compose run app python manage.py runserver

- subimos el server a la 127.0.0.1:8000
docker compose up

Ahora solo realizamos docker compose up - down 


POR ALGUNA RAZON, para utilizar el data (pymongo) necesitamos eliminar el ./data y volver a guardar los datos, sino saldra con "exited with code 14"
