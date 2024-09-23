# 🌟 Proyecto de Interfaz Gráfica para la Consulta de Datos MySQL

Este proyecto implementa una interfaz gráfica utilizando Tkinter para consultar y mostrar datos de tablas en una base de datos MySQL replicada. Permite seleccionar nodos de replicación y tablas específicas para obtener y mostrar sus datos.

## 📚 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)

## 🚀 Características

- Conexión a un nodo maestro y tres nodos esclavos de MySQL.
- Selección de tablas específicas en función del nodo seleccionado.
- Visualización de datos en una tabla dentro de la aplicación.

## 🛠️ Requisitos

- Python 3.x
- Bibliotecas de Python:
  - `mysql-connector-python`
  - `pandas`
  - `tkinter`

## 📥 Instalación

1. Clona el repositorio:

   ```bash

   git clone https://github.com/tu_usuario/nombre_del_repositorio.git
   cd nombre_del_repositorio

   ```
2. Instala las bibliotecas necesarias:

   ```bash

    pip install mysql-connector-python pandas

   ```

## 🖥️ Uso

1. Asegúrate de que tu servidor MySQL esté en funcionamiento y que la base de datos `replication_db` esté configurada correctamente.

2. Ejecuta el script de la aplicación:

    ```bash

   python nombre_del_script.py

   ```

3. La interfaz gráfica se abrirá, permitiéndote seleccionar un nodo de MySQL y una tabla correspondiente. Los datos de la tabla seleccionada se mostrarán en una vista de árbol.

4. Para refrescar los datos, puedes hacer clic en el botón "Recargar Datos".

## 💡 Ejemplo de Conexión

El código establece conexiones a los siguientes nodos y tablas:

- **Nodos:**
  - MySQL Master (Puerto 3306)
  - MySQL Slave 1 (Puerto 3307)
  - MySQL Slave 2 (Puerto 3308)
  - MySQL Slave 3 (Puerto 3309)

- **Tablas:**
  - MySQL Master: A, B, C, D
  - MySQL Slave 1: A, B, C, D
  - MySQL Slave 2: A, B
  - MySQL Slave 3: C, D
