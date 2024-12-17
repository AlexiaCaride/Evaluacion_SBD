# Ejercicio: Desarrollo e integración de scripts en Python

## Descrición

El objectivo de este ejercicio es desarrollar dos scripts en Python que interactúen con una API, una base de datos MongoDB y diversas herramientas para el manejo de datos. Además, se incluye opciones avanzadas para mejorar la funcionalidad e integración de la solución.

## Pasos de ejecución de los scripts

### Crear enviroment con conda

Primero, crea el entorno virtual utilizando el archivo `bicis_env.yml`:

```bash
conda env create --file bicis_env.yml
```

### Preparar los docker

Los pasos necesarios para preparar los docker, esto creara un docker de un script que se conecta a una api, que a su vez añadirá los datos a la base de datos del docker de mongo

**Crear la imagen dockerizda del script de conexionapi.py**

A continuación, sigue los pasos necesarios para crear un contenedor Docker para un script que se conecta a una API. Este script también se encargará de añadir los datos a la base de datos MongoDB que se encuentra en otro contenedor Docker.

```bash
docker build -t conexionapi .
```

**Levantar el docker-compose**

```bash
docker-compose up -d
```

### Exportar a csv la base de datos mongo

Para exportar los datos, ejecuta el siguiente script Python:

```bash
python exportarDataframe.py
```

## Subir imagen a docker hub

A continuación, los pasos para subir la imagen de conexionapi a Docker Hub:

**Iniciar sesion**

```bash
docker login
```

**Etiquetar la imagen**

Sustituyendo los elementos indicados por los correspondientes de tu imagen:

```bash
docker tag <imagen_id> <usuario_dockerhub>/<repositorio>:<etiqueta>
```

Por ejemplo, en mi caso sería:

```bash
docker tag sha256:bb05b3a52182e05cbf79545d878459a5845c8c27fbb9cd7d69641044f3ed3baa alexiacaride/conexionapi:latest
```

**Subir la imagen**

```bash
docker push alexiacaride/conexionapi:latest
```

## Usar las imagenes en el cloud de OpenStack

Para usar las imágenes en el entorno de OpenStack, crea la instancia desde la página de OpenStack [Visitar OpenStack](https://cloud.srv.cesga.es/project/instances/)


**Inicia sesión en tu cuenta de cesga con la ip de tu instancia**

Conéctate a tu instancia de OpenStack usando el siguiente comando (sustituye XXX.XXX.XXX.XXX por la IP de tu instancia):

```bash
 ssh -J xueduaXXX@hadoop.cesga.es cesgaxuser@XXX.XXX.XXX.XXX
```

**Copia el docker compose**

Usa un editor de texto como nano para crear o editar el archivo docker-compose.yml en tu instancia:

```bash
 nano docker-compose.yml
```

**Ejecuta el docker-compose**

Una vez copiado el archivo docker-compose.yml, ejecuta el siguiente comando para levantar los contenedores:

```bash
 docker compose up -d
```

## Comprueba que guarde datos con Mongo

Conéctate a la base de datos MongoDB dentro del contenedor Docker:


```bash
docker exec -it mongo mongosh
```

**Comprueba que existe la base de datos y no esté vacia**

Para ver las bases de datos disponibles y comprobar que la base de datos no está vacía, usa el siguiente comando:

```bash
show dbs
```
