# Flujo de negocio corregido

El sistema sigue este flujo:

1. **Catálogo de productos**
   - El usuario selecciona un producto.
   - Define la cantidad.
   - Lo agrega al carrito.

2. **Carrito de compras**
   - La tabla del carrito muestra los productos agregados.
   - El usuario marca qué productos entran al pedido.
   - El botón **Procesar pedido** crea un pedido pendiente.
   - El carrito NO procesa pagos directamente.

3. **Pedidos**
   - El pedido se registra en `data/pedidos.json`.
   - El pedido aparece en la tabla de Pedidos con estado `Pendiente`.
   - Desde la tabla de Pedidos se usa **Enviar a proceso de pago**.

4. **Pagos**
   - El módulo de pagos recibe el ID del pedido y el total exacto.
   - Al procesar un pago aprobado, el pedido cambia a estado `Pagado`.
   - El pago se registra en `data/pagos.json`.

Reglas aplicadas:

- No se puede crear pedido con carrito vacío.
- No se puede crear pedido sin dirección de envío.
- No se puede agregar más cantidad que el stock disponible.
- Al crear pedido se reserva/descuenta stock.
- Al cancelar pedido se restaura stock.
- El monto del pago debe ser exactamente igual al total del pedido.
- Un pedido cancelado o entregado no puede pagarse.
