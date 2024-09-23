# 🚀 Configuración de la replicación MySQL con Docker

Este documento describe los pasos para configurar una replicación MySQL usando Docker con un nodo maestro y tres nodos esclavos.

---

## 📡 Crear una red Docker para la replicación MySQL

```bash

docker network create mysql-replication

```
## 🟢 Configuración del nodo maestro (MySQL Master)

```bash

docker run --name mysql-master -p 3306:3306 --network=mysql-replication
-e MYSQL_ROOT_PASSWORD=micontrasena -d mysql:8.0 --server-id=1 --log-bin=mysql-bin

```
## 🔑 Acceder al contenedor del nodo maestro

```bash

docker exec -it mysql-master mysql -uroot -pmicontrasena

```
## 📋 Ejecutar los siguientes comandos SQL dentro del contenedor
```bash

CREATE USER 'udistrital'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'Slavepass123'; GRANT REPLICATION SLAVE ON . TO 'udistrital'@'%'; FLUSH PRIVILEGES; SHOW MASTER STATUS;

```

> [!NOTE]
> Guarda el valor de `MASTER_LOG_FILE` y `MASTER_LOG_POS` para usarlo en los esclavos.  
Ejemplo de resultado:

```bash

MASTER_LOG_FILE='mysql-bin.000003' MASTER_LOG_POS=1427

```
## 🔵 Configuración del nodo esclavo 1 (MySQL Slave 1)
```bash

docker run --name mysql-slave1 -p 3307:3306 --network=mysql-replication
-e MYSQL_ROOT_PASSWORD=contraslave1 -d mysql:8.0 --server-id=2

```
## 🔑 Acceder al contenedor del esclavo 1

```bash

docker exec -it mysql-slave1 mysql -uroot -pcontraslave1

```
## 📋 Ejecutar los siguientes comandos SQL dentro del contenedor del esclavo 1
```bash

CHANGE MASTER TO
    MASTER_HOST='mysql-master',
    MASTER_USER='udistrital',
    MASTER_PASSWORD='Slavepass123',
    MASTER_LOG_FILE='mysql-bin.000003', -- Sustituye por el valor obtenido del maestro
    MASTER_LOG_POS=1427; -- Sustituye por el valor obtenido del maestro

START SLAVE; SHOW SLAVE STATUS\G;

```
## 🟡 Configuración del nodo esclavo 2 (MySQL Slave 2)
```bash

docker run --name mysql-slave2 -p 3308:3306 --network=mysql-replication
-e MYSQL_ROOT_PASSWORD=contraslave2 -d mysql:8.0 --server-id=3

```

## 🔑 Acceder al contenedor del esclavo 2

```bash

docker exec -it mysql-slave2 mysql -uroot -pcontraslave2

```

## 📋 Ejecutar los siguientes comandos SQL dentro del contenedor del esclavo 2

```bash

CHANGE MASTER TO
    MASTER_HOST='mysql-master',
    MASTER_USER='udistrital',
    MASTER_PASSWORD='Slavepass123',
    MASTER_LOG_FILE='mysql-bin.000003', -- Sustituye por el valor obtenido del maestro
    MASTER_LOG_POS=1427; -- Sustituye por el valor obtenido del maestro

-- Replicar solo las tablas A y B
CHANGE REPLICATION FILTER REPLICATE_DO_TABLE = (replication_db.A, replication_db.B);

START SLAVE; SHOW SLAVE STATUS\G;

```

## 🟣 Configuración del nodo esclavo 3 (MySQL Slave 3)

```bash

docker run --name mysql-slave3 -p 3309:3306 --network=mysql-replication
-e MYSQL_ROOT_PASSWORD=contraslave3 -d mysql:8.0 --server-id=4

```

## 🔑 Acceder al contenedor del esclavo 3

```bash

docker exec -it mysql-slave3 mysql -uroot -pcontraslave3

```

## 📋 Ejecutar los siguientes comandos SQL dentro del contenedor del esclavo 3

```bash

CHANGE MASTER TO
    MASTER_HOST='mysql-master',
    MASTER_USER='udistrital',
    MASTER_PASSWORD='Slavepass123',
    MASTER_LOG_FILE='mysql-bin.000003', -- Sustituye por el valor obtenido del maestro
    MASTER_LOG_POS=1427; -- Sustituye por el valor obtenido del maestro

-- Replicar solo las tablas C y D
CHANGE REPLICATION FILTER REPLICATE_DO_TABLE = (replication_db.C, replication_db.D);

START SLAVE; SHOW SLAVE STATUS\G;

```

## ✅ Verificación de la replicación

Para cada nodo esclavo, ejecuta el siguiente comando para verificar el estado de la replicación:

```bash

SHOW SLAVE STATUS\G;

```

> [!TIP]
> Verifica que no haya errores en las columnas `Last_IO_Error` o `Last_SQL_Error` y que las columnas `Seconds_Behind_Master` estén en 0.

Con estos pasos, tendrás una replicación MySQL en Docker con un nodo maestro y tres nodos esclavos correctamente configurados.
