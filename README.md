# DAI

## IMPORTANTE

Para lo esté en requirements.txt
- docker compose build 

Ejecuta " python manage.py runserver 0.0.0.0:8000"
- docker compose up 


Autenticación: 
- http://localhost:8000/admin

  - User|password:
    - admin | admin
    - javier | password
    - juan | password

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


## Practica 5
crear front-end con Vite entonces

```
npm install react-bootstrap bootstrap

create-vite@latest
--
cd front
npm install
npm run dev
```

Descargar extension ES7+ REACT...

Para crear rapido un componente utilizar al principio de la pagina
```
rfc
```

npm install react-bootstrap bootstrap


## Practica 6
- Crear carpeta nginx y documentarlo con la configuración y el dockerfile (como está)
- Crear y añadir nginx docker-compose-prod 

```
docker compose -f ./docker-compose-prod.yml build
docker compose -f ./docker-compose-prod.yml up
```

- Cambiar las busquedas en react y la configuración para que se ejecuten los extras (en dist no se crea la carpeta public, directamente la de imagenes - a tener en cuenta en resultados.jsx)
```
npm run build
```

- Pasar las imagenes a static
- ejecutar docker compose y ya tenemos todo

```
localhost/
localhost/react
```