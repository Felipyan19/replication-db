# 🚀 Configuración de la replicación MySQL con Docker

Este documento describe los pasos para configurar una replicación MySQL usando Docker con un nodo maestro y tres nodos esclavos.

---

## 📡 Crear una red Docker para la replicación MySQL

```bash
docker network create mysql-replication

```

# Crear una red Docker para la replicación MySQL
docker network create mysql-replication

# Configuración del nodo maestro (MySQL Master)
docker run --name mysql-master -p 3306:3306 --network=mysql-replication -e MYSQL_ROOT_PASSWORD=micontrasena -d mysql:8.0 --server-id=1 --log-bin=mysql-bin

# Acceder al contenedor del nodo maestro
docker exec -it mysql-master mysql -uroot -pmicontrasena

# Dentro del contenedor del nodo maestro ejecutar los siguientes comandos SQL
CREATE USER 'udistrital'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'Slavepass123';
GRANT REPLICATION SLAVE ON *.* TO 'udistrital'@'%';
FLUSH PRIVILEGES;
SHOW MASTER STATUS;

# Guardar el valor de MASTER_LOG_FILE y MASTER_LOG_POS para usarlo en los esclavos
# Por ejemplo, el resultado podría ser:
# MASTER_LOG_FILE='mysql-bin.000003'
# MASTER_LOG_POS=1427

# Configuración del nodo esclavo 1 (MySQL Slave 1)
docker run --name mysql-slave1 -p 3307:3306 --network=mysql-replication -e MYSQL_ROOT_PASSWORD=contraslave1 -d mysql:8.0 --server-id=2

# Acceder al contenedor del esclavo 1
docker exec -it mysql-slave1 mysql -uroot -pcontraslave1

# Dentro del contenedor del esclavo 1 ejecutar los siguientes comandos SQL
CHANGE MASTER TO
    MASTER_HOST='mysql-master',
    MASTER_USER='udistrital',
    MASTER_PASSWORD='Slavepass123',
    MASTER_LOG_FILE='mysql-bin.000003',  -- Sustituye por el valor obtenido del maestro
    MASTER_LOG_POS=1427;                 -- Sustituye por el valor obtenido del maestro

START SLAVE;
SHOW SLAVE STATUS\G;

# Configuración del nodo esclavo 2 (MySQL Slave 2)
docker run --name mysql-slave2 -p 3308:3306 --network=mysql-replication -e MYSQL_ROOT_PASSWORD=contraslave2 -d mysql:8.0 --server-id=3

# Acceder al contenedor del esclavo 2
docker exec -it mysql-slave2 mysql -uroot -pcontraslave2

# Dentro del contenedor del esclavo 2 ejecutar los siguientes comandos SQL
CHANGE MASTER TO
    MASTER_HOST='mysql-master',
    MASTER_USER='udistrital',
    MASTER_PASSWORD='Slavepass123',
    MASTER_LOG_FILE='mysql-bin.000003',  -- Sustituye por el valor obtenido del maestro
    MASTER_LOG_POS=1427;                 -- Sustituye por el valor obtenido del maestro

# Replicar solo las tablas A y B
CHANGE REPLICATION FILTER REPLICATE_DO_TABLE = (replication_db.A, replication_db.B);

START SLAVE;
SHOW SLAVE STATUS\G;

# Configuración del nodo esclavo 3 (MySQL Slave 3)
docker run --name mysql-slave3 -p 3309:3306 --network=mysql-replication -e MYSQL_ROOT_PASSWORD=contraslave3 -d mysql:8.0 --server-id=4

# Acceder al contenedor del esclavo 3
docker exec -it mysql-slave3 mysql -uroot -pcontraslave3

# Dentro del contenedor del esclavo 3 ejecutar los siguientes comandos SQL
CHANGE MASTER TO
    MASTER_HOST='mysql-master',
    MASTER_USER='udistrital',
    MASTER_PASSWORD='Slavepass123',
    MASTER_LOG_FILE='mysql-bin.000003',  -- Sustituye por el valor obtenido del maestro
    MASTER_LOG_POS=1427;                 -- Sustituye por el valor obtenido del maestro

# Replicar solo las tablas C y D
CHANGE REPLICATION FILTER REPLICATE_DO_TABLE = (replication_db.C, replication_db.D);

START SLAVE;
SHOW SLAVE STATUS\G;

# Verificación de la replicación
# Para cada esclavo, ejecutar el siguiente comando para verificar el estado de la replicación:
SHOW SLAVE STATUS\G;