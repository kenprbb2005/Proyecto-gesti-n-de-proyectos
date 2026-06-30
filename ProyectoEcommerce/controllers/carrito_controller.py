from tkinter import messagebox

from views.carrito_view import CarritoView
from utils.ui import clear_tree, money
from controllers.helpers import get_selected_values


class CarritoController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.view = CarritoView(app_controller.content_frame, self)

    def on_show(self):
        self.load_cart()

    def _user_id(self):
        if not self.app_controller.current_user:
            raise ValueError("Debes iniciar sesión.")
        return self.app_controller.current_user.id_usuario

    def load_cart(self):
        try:
            carrito = self.app_controller.services.carrito_service.obtener_carrito_activo(self._user_id())
            items = self.app_controller.services.carrito_service.obtener_items_detallados(carrito)
            clear_tree(self.view.tabla)

            for item in items:
                marcado = "✓ Sí" if bool(item.get("seleccionado", True)) else "— No"
                estado_stock = self._estado_stock(item)
                self.view.tabla.insert(
                    "",
                    "end",
                    iid=item["id_producto"],
                    values=(
                        marcado,
                        item["id_producto"],
                        item["nombre"],
                        item["cantidad"],
                        money(item["precio_unitario"]),
                        money(item["subtotal"]),
                        estado_stock,
                    ),
                )

            totals = self.app_controller.services.carrito_service.totalizar(carrito, solo_seleccionados=True)
            hay_seleccionados = totals["cantidad_items"] > 0
            envio = self.app_controller.services.pedido_service.COSTOS_ENVIO.get(self.view.canton.get(), 3500)
            total = totals["total_parcial"] + envio if hay_seleccionados else 0
            self.view.set_totals(
                totals["subtotal"],
                totals["impuesto"],
                envio if hay_seleccionados else 0,
                total,
                totals["cantidad_items"],
                len(items),
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def _estado_stock(item):
        if item.get("estado_producto") != "Disponible":
            return item.get("estado_producto", "No disponible")
        cantidad = int(item.get("cantidad", 0))
        stock = int(item.get("stock_actual", 0))
        if cantidad > stock:
            return f"Stock insuficiente ({stock})"
        return f"Disponible ({stock})"

    def _selected_product_ids(self):
        selected = self.view.tabla.selection()
        ids = []
        for row_id in selected:
            values = self.view.tabla.item(row_id, "values")
            if values:
                ids.append(values[1])
        return ids

    def change_quantity(self, delta):
        values = get_selected_values(self.view.tabla)
        if not values:
            messagebox.showwarning("Carrito", "Selecciona un producto del carrito.")
            return
        try:
            id_producto = values[1]
            current = int(values[3])
            self.app_controller.services.carrito_service.actualizar_cantidad(
                self._user_id(),
                id_producto,
                current + delta,
            )
            self.load_cart()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_item(self):
        ids_productos = self._selected_product_ids()
        if not ids_productos:
            messagebox.showwarning("Carrito", "Selecciona uno o varios productos del carrito.")
            return
        try:
            for id_producto in ids_productos:
                self.app_controller.services.carrito_service.eliminar_producto(self._user_id(), id_producto)
            self.load_cart()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def empty_cart(self):
        try:
            if messagebox.askyesno("Carrito", "¿Deseas vaciar todo el carrito?"):
                self.app_controller.services.carrito_service.vaciar(self._user_id())
                self.load_cart()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mark_selected_for_purchase(self, seleccionado: bool):
        ids_productos = self._selected_product_ids()
        if not ids_productos:
            messagebox.showwarning("Carrito", "Selecciona uno o varios productos de la tabla.")
            return
        try:
            for id_producto in ids_productos:
                self.app_controller.services.carrito_service.seleccionar_producto(
                    self._user_id(),
                    id_producto,
                    seleccionado,
                )
            self.load_cart()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mark_all_for_purchase(self, seleccionado: bool):
        try:
            self.app_controller.services.carrito_service.seleccionar_todos(self._user_id(), seleccionado)
            self.load_cart()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_selected_purchase_event(self, event=None):
        if event is not None and hasattr(event, "y"):
            row = self.view.tabla.identify_row(event.y)
            if row:
                self.view.tabla.selection_set(row)
        self.toggle_selected_purchase()

    def toggle_selected_purchase(self):
        values = get_selected_values(self.view.tabla)
        if not values:
            return
        try:
            id_producto = values[1]
            self.app_controller.services.carrito_service.alternar_seleccion_producto(
                self._user_id(),
                id_producto,
            )
            self.load_cart()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def procesar_pedido(self):
        """Norma del negocio: el carrito crea un pedido y lo registra en la tabla Pedidos."""
        try:
            pedido = self.app_controller.services.pedido_service.crear_desde_carrito(
                self._user_id(),
                self.view.canton.get(),
                self.view.direccion.get(),
            )
            self.load_cart()
            messagebox.showinfo(
                "Pedido registrado",
                f"Pedido {pedido.id_pedido} registrado correctamente.\n\n"
                f"Total: {money(pedido.total)}\n"
                "Estado: Pendiente de pago.\n\n"
                "Ahora se abrirá la tabla de pedidos para continuar con el proceso de pago.",
            )
            pedidos_controller = self.app_controller.controllers["pedidos"]
            pedidos_controller.pedido_enfocado = pedido.id_pedido
            self.app_controller.show_view("pedidos")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Alias por compatibilidad con versiones anteriores del botón.
    def checkout(self):
        self.procesar_pedido()

    def checkout_and_pay(self):
        messagebox.showwarning(
            "Flujo corregido",
            "Según la norma del negocio, primero se procesa el pedido desde el carrito, luego se paga desde el módulo de pedidos/pagos.",
        )
        self.procesar_pedido()

    def go_to_catalogo(self):
        self.app_controller.show_view("catalogo")
