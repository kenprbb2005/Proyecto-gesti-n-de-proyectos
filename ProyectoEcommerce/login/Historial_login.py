import tkinter as tk
from tkinter import ttk

ventana = tk.Tk()
ventana.title("Módulo Historial de Compras")
ventana.geometry("1100x620")
ventana.configure(bg="#eef2f7")

style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background="#eef2f7")
style.configure("Card.TFrame", background="white", relief="flat")
style.configure("TLabel", background="white", font=("Segoe UI", 10))
style.configure("Title.TLabel", background="#eef2f7", font=("Segoe UI", 22, "bold"))
style.configure("Subtitle.TLabel", background="#eef2f7", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10), padding=8)
style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

header = ttk.Frame(ventana)
header.pack(fill="x", padx=25, pady=(20, 10))

ttk.Label(header, text="Historial de Compras", style="Title.TLabel").pack(anchor="w")
ttk.Label(header, text="Consulta visual del historial de compras realizadas por los usuarios.", style="Subtitle.TLabel").pack(anchor="w")

card = ttk.Frame(ventana, style="Card.TFrame")
card.pack(fill="x", padx=25, pady=10)

campos = [
    ("ID Historial", 0, 0),
    ("ID Usuario", 0, 2),
    ("ID Compra", 1, 0),
    ("Acción", 1, 2),
    ("Descripción", 2, 0),
    ("Fecha", 2, 2),
]

for texto, fila, columna in campos:
    ttk.Label(card, text=texto).grid(row=fila, column=columna, padx=15, pady=12, sticky="w")
    ttk.Entry(card, width=32).grid(row=fila, column=columna + 1, padx=15, pady=12)

botones = ttk.Frame(ventana)
botones.pack(fill="x", padx=25, pady=10)

ttk.Button(botones, text="Registrar").pack(side="left", padx=5)
ttk.Button(botones, text="Editar").pack(side="left", padx=5)
ttk.Button(botones, text="Eliminar").pack(side="left", padx=5)
ttk.Button(botones, text="Buscar").pack(side="left", padx=5)
ttk.Button(botones, text="Limpiar").pack(side="left", padx=5)

tabla_frame = ttk.Frame(ventana)
tabla_frame.pack(fill="both", expand=True, padx=25, pady=10)

tabla = ttk.Treeview(
    tabla_frame,
    columns=("id_historial", "id_usuario", "id_compra", "accion", "descripcion", "fecha"),
    show="headings"
)

encabezados = {
    "id_historial": "ID Historial",
    "id_usuario": "ID Usuario",
    "id_compra": "ID Compra",
    "accion": "Acción",
    "descripcion": "Descripción",
    "fecha": "Fecha"
}

for columna, texto in encabezados.items():
    tabla.heading(columna, text=texto)
    tabla.column(columna, width=160)

scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scroll.set)

tabla.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

ventana.mainloop()