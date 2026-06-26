# Proyecto Ecommerce MVC con JSON

Sistema académico en Python/Tkinter con arquitectura MVC y persistencia local en archivos JSON.

## Cómo ejecutar

```bash
cd ProyectoEcommerce
python main.py
```

## Usuarios demo

Administrador:
- Correo: admin@demo.com
- Contraseña: admin123

Cliente:
- Correo: cliente@demo.com
- Contraseña: cliente123

## Flujo para realizar una compra

1. Inicia sesión como cliente.
2. Entra al catálogo.
3. Selecciona un producto.
4. Indica la cantidad.
5. Presiona **Agregar al carrito**.
6. Entra a **Carrito de compras**.
7. Escribe una dirección de envío.
8. Selecciona provincia, método de pago y referencia.
9. Presiona **Realizar compra completa**.

El sistema crea el pedido, procesa el pago simulado, descuenta inventario, registra historial y genera notificaciones.

Regla de prueba: si la referencia del pago termina en `0000`, el pago se rechaza y el sistema cancela el pedido restaurando el stock.

## Módulos incluidos

- Usuarios
- Autenticación login/registro/recuperación
- Catálogo de productos
- Categorías
- Carrito de compras
- Órdenes/pedidos
- Pagos simulados
- Historial de compras
- Inventario
- Reseñas
- Notificaciones
- Panel administrativo

## Persistencia

Todos los datos se guardan en la carpeta `data/` usando archivos JSON.
