import tkinter as tk
from tkinter import ttk

class PanelAdminView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Main.TFrame")
        self.controller = controller

        contenedor = ttk.Frame(self, style="Main.TFrame")
        contenedor.pack(fill="both", expand=True, padx=30, pady=25)

        ttk.Label(contenedor, text="Panel Administrativo", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Resumen general del sistema y accesos rápidos a los módulos de gestión.",
            style="Subheader.TLabel"
        ).pack(anchor="w", pady=(0, 20))

        # Tarjetas de métricas (resumen visual)
        metricas_frame = ttk.Frame(contenedor, style="Main.TFrame")
        metricas_frame.pack(fill="x", pady=10)

        metricas = [
            ("Usuarios registrados", "1,248"),
            ("Productos en inventario", "356"),
            ("Pagos procesados", "892"),
            ("Reseñas publicadas", "1,074"),
        ]

        for i, (titulo, valor) in enumerate(metricas):
            tarjeta = ttk.Frame(metricas_frame, style="Card.TFrame")
            tarjeta.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
            ttk.Label(tarjeta, text=valor, font=("Segoe UI", 26, "bold"), background="white").pack(padx=25, pady=(18, 2))
            ttk.Label(tarjeta, text=titulo, background="white").pack(padx=25, pady=(0, 18))
            metricas_frame.columnconfigure(i, weight=1)

        # Accesos rápidos a los módulos de gestión
        accesos_card = ttk.Frame(contenedor, style="Card.TFrame")
        accesos_card.pack(fill="x", pady=20)

        ttk.Label(accesos_card, text="Accesos Rápidos", style="Title.TLabel", background="white").pack(anchor="w", padx=18, pady=(15, 5))

        accesos_botones = ttk.Frame(accesos_card, style="Card.TFrame")
        accesos_botones.pack(fill="x", padx=18, pady=(0, 18))

        modulos = [
            ("Inventario", "inventario"),
            ("Pagos", "pagos"),
            ("Reseñas", "resenas"),
            ("Historial", "historial"),
            ("Usuarios", "usuarios"),
            ("Notificaciones", "notificaciones"),
        ]

        for texto, vista in modulos:
            ttk.Button(
                accesos_botones,
                text=texto,
                command=lambda v=vista: self.controller.ir_a_modulo(v)
            ).pack(side="left", padx=5)

        # Actividad reciente (tabla informativa)
        ttk.Label(contenedor, text="Actividad Reciente", style="Title.TLabel").pack(anchor="w", pady=(10, 5))

        tabla_frame = ttk.Frame(contenedor, style="Card.TFrame")
        tabla_frame.pack(fill="both", expand=True, pady=10)

        tabla = ttk.Treeview(
            tabla_frame,
            columns=("fecha", "usuario", "modulo", "accion"),
            show="headings"
        )

        encabezados = {
            "fecha": "Fecha",
            "usuario": "Usuario",
            "modulo": "Módulo",
            "accion": "Acción"
        }

        for columna, texto in encabezados.items():
            tabla.heading(columna, text=texto)
            tabla.column(columna, width=180)

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll_y.set)

        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)
