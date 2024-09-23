import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import ttk

def fetch_data(db_name):
    # Conexión a la base de datos
    try:
        conn = mysql.connector.connect(
        user= 'root',
        password= 'micontrasena',  
        host= '127.0.0.1',  
        port= '3306', 
        database="replication_db"
        )
        query = "SELECT id, name FROM A"  # Asegúrate de que la tabla A exista en ambas bases de datos
        df = pd.read_sql(query, conn)
        return df

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if conn:
            conn.close()

# Función para poblar la tabla
def populate_table():
    db_name = db_combobox.get()  # Obtener el nombre de la base de datos seleccionada
    df = fetch_data(db_name)
    if df is not None and not df.empty:
        # Limpiar la tabla antes de cargar nuevos datos
        for item in tree.get_children():
            tree.delete(item)
        
        for index, row in df.iterrows():
            tree.insert("", tk.END, values=(row['id'], row['name']))

# Crear ventana principal
root = tk.Tk()
root.title("Datos de la Tabla A")

# ComboBox para seleccionar la base de datos
db_combobox = ttk.Combobox(root, values=["replication_db", "otra_base_de_datos"])  # Agrega los nombres de tus bases de datos
db_combobox.set("Selecciona una base de datos")  # Texto por defecto
db_combobox.pack(pady=10)

# Crear tabla
tree = ttk.Treeview(root, columns=("ID", "Name"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.pack(fill=tk.BOTH, expand=True)

# Cargar datos automáticamente al seleccionar base de datos
db_combobox.bind("<<ComboboxSelected>>", lambda e: populate_table())

# Botón para recargar datos
load_button = tk.Button(root, text="Recargar Datos", command=populate_table)
load_button.pack(pady=10)

# Iniciar la aplicación
root.mainloop()