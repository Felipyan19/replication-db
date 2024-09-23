import tkinter as tk
from tkinter import ttk
from database import fetch_data, get_tables
from utils import get_key_by_value

name_port = {
    "MySQL Master": "3306",
    "MySQL Slave 1": "3307",
    "MySQL Slave 2": "3308",
    "MySQL Slave 3": "3309"
}

def create_gui():
    root = tk.Tk()
    root.title("Datos de replicación")

    # Combobox para seleccionar el puerto
    names_of_port = list(name_port.keys())
    port_combobox = ttk.Combobox(root, values=names_of_port)
    port_combobox.set("Selecciona un nodo") 
    port_combobox.pack(pady=10)

    # Combobox para seleccionar la tabla
    table_combobox = ttk.Combobox(root, values=[])
    table_combobox.set("Selecciona una tabla")  
    table_combobox.pack(pady=10)

    # Tabla para mostrar los datos
    tree = ttk.Treeview(root, columns=("ID", "Name"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.pack(fill=tk.BOTH, expand=True)

    def update_table_combobox(event):
        table_combobox.set("Selecciona una tabla")
        port = name_port[port_combobox.get()]
        df = get_tables(port)
        if df is not None and not df.empty:
            table_combobox['values'] = df['Tables_in_replication_db'].tolist()

    def populate_table():
        port = name_port[port_combobox.get()]
        table = table_combobox.get()
        if table != "Selecciona una tabla":
            df = fetch_data(port, table)
            if df is not None and not df.empty:
                for item in tree.get_children():
                    tree.delete(item)
                for _, row in df.iterrows():
                    tree.insert("", tk.END, values=(row['id'], row['name']))

    port_combobox.bind("<<ComboboxSelected>>", update_table_combobox)
    table_combobox.bind("<<ComboboxSelected>>", lambda e: populate_table())

    load_button = tk.Button(root, text="Recargar Datos", command=populate_table)
    load_button.pack(pady=10)

    root.mainloop()
