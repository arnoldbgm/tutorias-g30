# 🧠 PROMPT COMPLETO PARA GENERAR EL PROYECTO

Puedes copiar esto tal cual:

---

Quiero que actúes como un **arquitecto backend senior experto en Django 5 y Django Rest Framework**, enfocado en buenas prácticas, escalabilidad y código listo para producción.

Necesito que generes un proyecto completo de API para una tienda virtual con las siguientes características:

---

# 🧱 STACK TECNOLÓGICO

* Django 5
* Django Rest Framework
* Sqlite 
* Autenticación con JWT (SimpleJWT)
* Configuración basada en variables de entorno (.env)
* Estructura modular por apps

---

# 📁 ESTRUCTURA DEL PROYECTO

Organiza el proyecto en apps separadas:

* users
* addresses
* catalog
* cart
* orders
* payments
* shipments
* common (utilidades compartidas)

Incluye:

* settings modular (base.py, dev.py, prod.py)
* carpeta `core` para configuraciones globales

---

# 🧑‍💻 MODELO DE USUARIO

* Implementar un modelo de usuario personalizado
* Login con email en lugar de username
* Usar AbstractBaseUser
* Campos:

  * id 
  * email (único)
  * first_name
  * last_name
  * is_active
  * is_staff
  * date_joined

---

# 📍 ADDRESSES

Modelo Address:

* user (FK)
* full_name
* phone
* address_line_1
* address_line_2
* city
* state
* country
* postal_code
* is_default

---

# 🛍️ CATÁLOGO

## Category

* name
* slug
* parent (self FK)

## Product

* name
* slug
* description
* category (FK)
* brand
* is_active

## ProductVariant

* product (FK)
* sku (único)
* name
* price
* compare_price
* stock
* weight
* is_active

## ProductImage

* product (FK)
* image
* alt_text
* is_main

---

# 🛒 CARRITO

## Cart

* user (nullable)
* session_key

## CartItem

* cart (FK)
* product_variant (FK)
* quantity

---

# 📦 ÓRDENES

## Order

* user (FK)
* status (pending, paid, shipped, delivered, cancelled)
* total_amount
* shipping_address (JSON snapshot)
* billing_address (JSON snapshot)

## OrderItem

* order (FK)
* product_variant (FK)
* product_name (snapshot)
* sku (snapshot)
* price
* quantity
* total

---

# 💳 PAGOS

## Payment

* order (FK)
* provider
* transaction_id
* amount
* status
* paid_at

---

# 🚚 ENVÍOS

## Shipment

* order (FK)
* tracking_number
* carrier
* status
* shipped_at
* delivered_at

---

# ⚙️ REGLAS IMPORTANTES

* Agregar timestamps (created_at, updated_at)
* Usar soft delete si es posible
* Validaciones en serializers, no en views
* Separar lógica de negocio en services
* Usar select_related y prefetch_related donde corresponda
* Evitar lógica en views (usar ViewSets limpios)

---

# 🔌 API (DRF)

Generar:

* Serializers para todos los modelos
* ViewSets
* Routers automáticos
* Paginación global
* Filtros (DjangoFilterBackend)
* Búsqueda básica en productos

---

# 🔐 AUTENTICACIÓN

* JWT con SimpleJWT
* Endpoints:

  * login
  * refresh
  * register

---

# 💡 FUNCIONALIDADES CLAVE

Implementar lógica para:

1. Agregar productos al carrito
2. Actualizar cantidades
3. Crear orden desde carrito
4. Calcular total correctamente
5. Crear pago asociado a orden
6. Cambiar estado de orden según pago

---

# 🧪 BUENAS PRÁCTICAS

* Código limpio y tipado
* Uso de signals solo si es necesario
* Evitar lógica duplicada
* Manejo de errores consistente

---

# 🚀 OPCIONAL (SI PUEDES)

* Makefile
* Fixtures iniciales
* Swagger (drf-spectacular o similar)

---

# 🎯 FORMATO DE RESPUESTA

Quiero que generes el proyecto paso a paso:

1. Estructura de carpetas
2. settings
3. modelos
4. serializers
5. views
6. urls
7. servicios (business logic)
8. configuración final

No omitas código importante.

