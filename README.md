# Resumen

Este proyecto es un pipeline que se encarga de mover los datos desde una base de datos (`source`) a otra (`destination`). Esto utilizando PostgreSQL, Docker y Python.

## Airflow

Para iniciar el proyecto utilice el siguiente comando:

```bash
docker compose up
```

Despues de eso se podra utilizar la aplicacion o interfaz de airflow en el http://localhost:8080/

El usuario y contraseña configurado por defecto son los siguientes:
- username: `airflow`
- password: `password`

## Comandos

**Iniciar el pipeline**

```bash
docker compose up
```

> Este comando creara las dos base de datos, agregara los datos iniciales a la base de datos `source` y luego se moveran los datos a `destination` utilizando Python (`elt/elt_script.py`).


luego se puede acceder a la base de datos `destination` con:

```bash
docker compose exec -it destination_postgres psql -U harold -d destination_db
```

y por ultimo listar las bases de datos:

```
\dt
```

Output:
```
            List of relations
 Schema |     Name      | Type  | Owner  
--------+---------------+-------+--------
 public | actors        | table | harold
 public | film_actors   | table | harold
 public | film_category | table | harold
 public | films         | table | harold
 public | users         | table | harold
(5 rows)
```

