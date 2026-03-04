# Basic Checkout — Django E-Commerce System

> **Proyecto académico desarrollado con fines educativos.**  
> Entrega final para la materia **Modelado de Aplicaciones Web**  
> Maestría en Sistemas Computacionales

---

## Índice

1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Propósito académico](#2-propósito-académico)
3. [Stack tecnológico](#3-stack-tecnológico)
4. [Arquitectura del sistema](#4-arquitectura-del-sistema)
5. [Estructura de archivos](#5-estructura-de-archivos)
6. [Principios SOLID](#6-principios-solid)
7. [Patrones de diseño](#7-patrones-de-diseño)
8. [Modelos de datos](#8-modelos-de-datos)
9. [Flujo de la aplicación](#9-flujo-de-la-aplicación)
10. [Protección de URLs y seguridad](#10-protección-de-urls-y-seguridad)
11. [Instalación y ejecución](#11-instalación-y-ejecución)

---

## 1. Descripción del proyecto

**Basic Checkout** es un sistema de comercio electrónico básico construido con Django que implementa el flujo completo de compra en línea:

- Catálogo de productos con stock en tiempo real
- Carrito de compras persistente (usuarios autenticados y anónimos)
- Proceso de checkout con captura de dirección de envío
- Gestión de órdenes con historial por usuario
- Autenticación y gestión de cuentas vía django-allauth

El objetivo del proyecto es demostrar cómo aplicar **principios de diseño de software de nivel empresarial** (SOLID, patrones GoF) dentro del ecosistema Django, produciendo código mantenible, extensible y testeable.

---

## 2. Propósito académico

| Campo | Detalle                                                                    |
|---|----------------------------------------------------------------------------|
| **Institución** | TecNM Campus Zamora                                                        |
| **Materia** | Modelado de Aplicaciones Web                                               |
| **Tipo** | Proyecto de entrega final                                                  |
| **Propósito** | Educativo / Demostración de conceptos                                      |
| **Enfoque** | Aplicación práctica de SOLID y patrones de diseño en un framework web real |

Este proyecto **no está destinado a producción**. Su función es ilustrar de manera concreta y ejecutable cómo los principios teóricos de ingeniería de software se traducen en decisiones de arquitectura dentro de una aplicación web completa.

---

## 3. Stack tecnológico

| Capa | Tecnología |
|---|---|
| **Backend** | Python 3.12 + Django 4.2 |
| **Autenticación** | django-allauth |
| **Base de datos** | SQLite (desarrollo) |
| **Frontend** | Django Templates + Tailwind CSS (Play CDN) |
| **Tipografías** | Space Mono, Syne (Google Fonts) |

---

## 4. Arquitectura del sistema

El proyecto sigue una **arquitectura en capas** estricta. Cada capa tiene una responsabilidad única y se comunica solo con la capa inmediatamente inferior:

```
┌─────────────────────────────────────────────┐
│               PRESENTATION LAYER            │
│         Templates (HTML + Tailwind)         │
└────────────────────┬────────────────────────┘
                     │ HTTP Request / Response
┌────────────────────▼────────────────────────┐
│                  VIEW LAYER                 │
│     Class-Based Views (thin controllers)    │
│   Solo maneja HTTP, delega toda la lógica   │
└────────────────────┬────────────────────────┘
                     │ Llama a servicios
┌────────────────────▼────────────────────────┐
│               SERVICE LAYER                 │
│     CartService / CheckoutService           │
│   Toda la lógica de negocio vive aquí       │
└────────────────────┬────────────────────────┘
                     │ Accede a datos vía repositorios
┌────────────────────▼────────────────────────┐
│             REPOSITORY LAYER                │
│   ProductRepository / CartRepository /      │
│   OrderRepository (abstracción del ORM)     │
└────────────────────┬────────────────────────┘
                     │ Queries al ORM
┌────────────────────▼────────────────────────┐
│                DATA LAYER                   │
│            Django ORM + SQLite              │
└─────────────────────────────────────────────┘
```

Esta separación garantiza que cambiar la base de datos, el ORM, o incluso el framework web, impacte solo la capa afectada y no el resto del sistema.

---

## 5. Estructura de archivos

```
basic_checkout/
│
├── manage.py                        # Entry point de Django
├── requirements.txt                 # Dependencias del proyecto
│
├── config/                          # Configuración central
│   ├── settings.py                  # Settings de Django
│   ├── urls.py                      # Router raíz con comentarios de seguridad
│   └── wsgi.py
│
├── core/                            # Módulo base compartido
│   ├── models.py                    # TimestampedModel, UUIDModel (abstractos)
│   ├── repositories.py              # BaseRepository[T] genérico
│   ├── exceptions.py                # Excepciones de dominio custom
│   └── templates/
│       ├── base.html                # Template maestro con Tailwind CDN
│       └── account/                 # Overrides de django-allauth
│           ├── login.html
│           ├── signup.html
│           └── password_reset.html
│
├── products/                        # App: catálogo de productos
│   ├── models.py                    # Category, Product
│   ├── repositories.py              # ProductRepository, CategoryRepository
│   ├── views.py                     # ProductListView, ProductDetailView
│   ├── urls.py
│   └── templates/products/
│       ├── product_list.html
│       └── product_detail.html
│
├── cart/                            # App: carrito de compras
│   ├── models.py                    # Cart, CartItem
│   ├── repositories.py              # CartRepository, CartItemRepository
│   ├── services.py                  # CartService (lógica de negocio)
│   ├── views.py                     # Add / Remove / Update / Detail
│   ├── urls.py
│   └── templates/cart/
│       └── cart_detail.html
│
└── checkout/                        # App: órdenes y checkout
    ├── models.py                    # Order, OrderItem
    ├── forms.py                     # CheckoutForm (dirección + contacto)
    ├── repositories.py              # OrderRepository, OrderItemRepository
    ├── services.py                  # CheckoutService + PaymentStrategy + OrderFactory
    ├── views.py                     # Checkout / Confirmation / History / Detail
    ├── urls.py
    └── templates/checkout/
        ├── checkout.html
        ├── order_confirmation.html
        ├── order_history.html
        └── order_detail.html
```

**Métricas del proyecto:**

| Métrica | Valor |
|---|---|
| Líneas de código Python | ~1,100 |
| Archivos Python | 20 |
| Templates HTML | 11 |
| Apps Django | 4 |
| Modelos | 6 (Category, Product, Cart, CartItem, Order, OrderItem) |

---

## 6. Principios SOLID

Los cinco principios SOLID se aplican de forma explícita y trazable en el código.

### S — Single Responsibility Principle

> *"Una clase debe tener una sola razón para cambiar."*

Cada clase tiene exactamente una responsabilidad bien definida. El sistema está dividido en capas donde ninguna clase hace más de lo que le corresponde:

| Clase | Su única responsabilidad |
|---|---|
| `ProductRepository` | Ejecutar queries de productos contra la base de datos |
| `CartService` | Aplicar las reglas de negocio del carrito |
| `CheckoutForm` | Validar los datos del formulario de envío |
| `OrderFactory` | Construir instancias de `Order` y `OrderItem` |
| `CartDetailView` | Manejar la request HTTP del carrito (nada más) |

**Ejemplo concreto** — `CartDetailView` no contiene ninguna lógica de negocio. Solo resuelve el carrito y renderiza el template:

```python
# cart/views.py
class CartDetailView(View):
    def get(self, request):
        cart = self._cart_service.get_or_create_cart(request)  # delega
        return render(request, "cart/cart_detail.html", {"cart": cart})
```

Si la lógica del carrito cambia, `CartDetailView` no necesita modificarse. Si la presentación cambia, `CartService` no se ve afectado.

---

### O — Open/Closed Principle

> *"Las entidades de software deben estar abiertas para extensión, pero cerradas para modificación."*

Los modelos base abstractos permiten agregar nuevas entidades sin tocar el código existente:

```python
# core/models.py
class UUIDModel(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta:
        abstract = True
```

Cualquier nuevo modelo (`Product`, `Cart`, `Order`, etc.) extiende `UUIDModel` y hereda automáticamente UUID como PK y los campos de timestamp. Agregar un nuevo modelo no modifica `UUIDModel`.

El ejemplo más claro es el **patrón Strategy** aplicado al pago:

```python
# checkout/services.py
class PaymentStrategy(ABC):
    @abstractmethod
    def process(self, amount: Decimal, order: Order) -> PaymentResult:
        raise NotImplementedError

class DummyPaymentStrategy(PaymentStrategy): ...  # desarrollo
class StripePaymentStrategy(PaymentStrategy): ...  # producción (extensión)
```

Para agregar PayPal, se crea `PayPalPaymentStrategy(PaymentStrategy)` sin modificar `CheckoutService` ni ninguna estrategia existente.

---

### L — Liskov Substitution Principle

> *"Los objetos de una subclase deben poder sustituir a los de su superclase sin alterar el comportamiento del programa."*

Todos los repositorios concretos son intercambiables con `BaseRepository[T]`. `CheckoutService` acepta cualquier `OrderRepository` sin importar su implementación concreta:

```python
# core/repositories.py
class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, pk) -> Optional[T]: ...

    @abstractmethod
    def save(self, entity: T) -> T: ...
```

```python
# checkout/repositories.py
class OrderRepository(BaseRepository[Order]):
    def get_by_id(self, pk) -> Optional[Order]: ...  # implementación concreta
    def save(self, entity: Order) -> Order: ...
```

Si se quisiera cambiar la persistencia de órdenes a una API REST en lugar de SQLite, bastaría con crear `RestOrderRepository(BaseRepository[Order])` e inyectarlo. El `CheckoutService` funcionaría sin cambios.

---

### I — Interface Segregation Principle

> *"Los clientes no deben depender de interfaces que no utilizan."*

En lugar de tener un único repositorio "universal", cada dominio tiene su propio repositorio con solo los métodos que necesita:

```
BaseRepository[T]      →  get_by_id, get_all, save, delete  (contrato mínimo)
     │
     ├── ProductRepository   →  + get_by_slug, get_available
     ├── CartRepository      →  + get_by_user, get_by_session, get_or_create_for_user
     ├── CartItemRepository  →  + get_by_cart_and_product
     └── OrderRepository     →  + get_by_user
```

`CartService` solo depende de `CartRepository` y `CartItemRepository`, nunca de `OrderRepository`. Los dominios están correctamente segregados.

---

### D — Dependency Inversion Principle

> *"Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones."*

`CheckoutService` (módulo de alto nivel) no instancia sus dependencias directamente. Las recibe como parámetros con valores por defecto, lo que permite inyectar implementaciones alternativas (especialmente útil para testing):

```python
# checkout/services.py
class CheckoutService:
    def __init__(
        self,
        payment_strategy: Optional[PaymentStrategy] = None,   # abstracción
        order_repo: Optional[OrderRepository] = None,          # abstracción
        order_item_repo: Optional[OrderItemRepository] = None, # abstracción
        order_factory: Optional[OrderFactory] = None,          # abstracción
        cart_service: Optional[CartService] = None,            # abstracción
    ):
        self._payment = payment_strategy or DummyPaymentStrategy()
        self._order_repo = order_repo or OrderRepository()
        # ...
```

Para hacer testing unitario de `CheckoutService`, se pueden inyectar mocks:

```python
# Ejemplo de test (no incluido en el proyecto)
service = CheckoutService(
    payment_strategy=MockPaymentStrategy(),
    order_repo=InMemoryOrderRepository(),
)
```

---

## 7. Patrones de diseño

Se implementan cuatro patrones del catálogo GoF (Gang of Four).

### 7.1 Repository Pattern

**Categoría:** Arquitectural  
**Propósito:** Aislar completamente el acceso a datos del resto de la aplicación.

**Problema que resuelve:** Si las vistas y servicios hacen queries directamente con el ORM, están acoplados a Django y a SQLite. Un cambio de base de datos requeriría modificar decenas de archivos.

**Solución:** Todo acceso a datos pasa por un repositorio. El repositorio es la única clase que "conoce" el ORM.

```
Vista / Servicio  →  Repository  →  Django ORM  →  SQLite
                     (abstrae)       (concreto)
```

```python
# products/repositories.py
class ProductRepository(BaseRepository[Product]):

    def get_available(self) -> List[Product]:
        """El ORM vive aquí. Nadie más lo toca."""
        return list(
            Product.objects.select_related("category").filter(
                is_active=True, stock__gt=0
            )
        )
```

```python
# products/views.py  — la vista no sabe que existe Django ORM
class ProductListView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._product_repo = ProductRepository()  # depende de la abstracción

    def get(self, request):
        products = self._product_repo.get_available()  # sin ORM directo
        return render(request, "products/product_list.html", {"products": products})
```

---

### 7.2 Service Layer Pattern

**Categoría:** Arquitectural  
**Propósito:** Concentrar toda la lógica de negocio en una capa dedicada, fuera de vistas y modelos.

**Problema que resuelve:** En Django es común poner lógica de negocio en las vistas ("fat views") o en los modelos ("fat models"). Ambos enfoques dificultan el testing y la reutilización.

**Solución:** Las vistas son controladores delgados. Toda la lógica vive en el servicio.

`CartService` orquesta el flujo completo de agregar un producto al carrito con todas sus reglas:

```python
# cart/services.py
class CartService:

    def add_item(self, request, product_id, quantity=1) -> CartItem:
        # Regla 1: el producto debe existir y estar activo
        product = self._product_repo.get_by_id(product_id)
        if product is None:
            raise ValueError(f"Product {product_id} not found.")

        # Regla 2: resolver el carrito (usuario o sesión anónima)
        cart = self.get_or_create_cart(request)
        existing_item = self._item_repo.get_by_cart_and_product(cart, product)
        new_quantity = (existing_item.quantity if existing_item else 0) + quantity

        # Regla 3: validar stock disponible
        if not product.has_sufficient_stock(new_quantity):
            raise InsufficientStockError(product.name, product.stock)

        # Regla 4: actualizar o crear el item
        if existing_item:
            existing_item.quantity = new_quantity
            return self._item_repo.save(existing_item)

        item = CartItem(cart=cart, product=product, quantity=quantity)
        return self._item_repo.save(item)
```

La vista correspondiente es trivialmente simple:

```python
# cart/views.py
class AddToCartView(View):
    def post(self, request, product_id):
        quantity = int(request.POST.get("quantity", 1))
        item = self._cart_service.add_item(request, product_id, quantity)
        messages.success(request, f"'{item.product.name}' added to your cart.")
        return redirect(...)
```

---

### 7.3 Strategy Pattern

**Categoría:** Comportamental ([GoF](https://www.geeksforgeeks.org/system-design/gang-of-four-gof-design-patterns/))  
**Propósito:** Definir una familia de algoritmos intercambiables y encapsular cada uno en su propia clase.

**Problema que resuelve:** El sistema de pago puede cambiar (Stripe, PayPal, transferencia bancaria). Si la lógica de pago está hardcodeada en `CheckoutService`, cada cambio requiere modificarlo.

**Solución:** Se define una interfaz abstracta `PaymentStrategy`. `CheckoutService` trabaja con la abstracción, sin conocer la implementación concreta.

```
                    ┌─────────────────────────┐
                    │    <<abstract>>         │
                    │   PaymentStrategy       │
                    │  + process(amount, order)│
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
   ┌──────────▼──────┐ ┌────────▼────────┐ ┌──────▼──────────┐
   │ DummyPayment    │ │ StripePayment   │ │ PayPalPayment   │
   │ Strategy        │ │ Strategy        │ │ Strategy (futura)│
   │ (desarrollo)    │ │ (producción)    │ │                 │
   └─────────────────┘ └─────────────────┘ └─────────────────┘
```

```python
# checkout/services.py
class PaymentStrategy(ABC):
    @abstractmethod
    def process(self, amount: Decimal, order: Order) -> PaymentResult:
        raise NotImplementedError

class DummyPaymentStrategy(PaymentStrategy):
    """Siempre aprueba — solo para desarrollo/demo."""
    def process(self, amount, order):
        return PaymentResult(success=True, transaction_id=str(uuid.uuid4()))

class StripePaymentStrategy(PaymentStrategy):
    """Integración real con Stripe."""
    def __init__(self, api_key: str):
        self._api_key = api_key
    def process(self, amount, order):
        # stripe.PaymentIntent.create(...)
        raise NotImplementedError("Pendiente de configurar.")
```

Cambiar el procesador de pago es una línea de código en la instanciación del servicio:

```python
# En producción:
checkout_service = CheckoutService(
    payment_strategy=StripePaymentStrategy(api_key=settings.STRIPE_SECRET_KEY)
)
```

---

### 7.4 Factory Pattern

**Categoría:** Creacional (GoF)  
**Propósito:** Encapsular la lógica de construcción de objetos complejos en una clase dedicada.

**Problema que resuelve:** Crear una `Order` desde un `Cart` implica lógica no trivial: calcular subtotales, agregar costo de envío, hacer snapshot de precios actuales. Si esto vive en `CheckoutService`, el servicio se vuelve demasiado grande.

**Solución:** `OrderFactory` es responsable exclusivamente de construir las instancias. `CheckoutService` delega la construcción.

```python
# checkout/services.py
class OrderFactory:
    SHIPPING_COST = Decimal("5.00")

    def build(self, cart: Cart, user, shipping_data: dict) -> Order:
        """Construye el objeto Order con todos los totales calculados."""
        subtotal = cart.total_price
        return Order(
            user=user,
            subtotal=subtotal,
            shipping_cost=self.SHIPPING_COST,
            total=subtotal + self.SHIPPING_COST,
            **shipping_data,
        )

    def build_items(self, order: Order, cart: Cart) -> list[OrderItem]:
        """
        Construye los OrderItems COPIANDO el precio actual del producto.
        Snapshot crítico: si el precio cambia mañana, la orden histórica
        debe conservar el precio al momento de la compra.
        """
        return [
            OrderItem(
                order=order,
                product=item.product,
                product_name=item.product.name,   # snapshot del nombre
                unit_price=item.product.price,     # snapshot del precio
                quantity=item.quantity,
            )
            for item in cart.items.select_related("product").all()
        ]
```

`CheckoutService` usa la factory sin preocuparse por cómo se construye la orden:

```python
# checkout/services.py — método place_order
order = self._factory.build(cart, user, shipping_data)     # Factory
self._order_repo.save(order)
items = self._factory.build_items(order, cart)             # Factory
for item in items:
    self._item_repo.save(item)
```

---

### Resumen de patrones y su ubicación

| Patrón | Archivo | Clases involucradas |
|---|---|---|
| **Repository** | `*/repositories.py` | `BaseRepository`, `ProductRepository`, `CartRepository`, `OrderRepository` |
| **Service Layer** | `cart/services.py`, `checkout/services.py` | `CartService`, `CheckoutService` |
| **Strategy** | `checkout/services.py` | `PaymentStrategy`, `DummyPaymentStrategy`, `StripePaymentStrategy` |
| **Factory** | `checkout/services.py` | `OrderFactory` |

---

## 8. Modelos de datos

```
┌──────────────┐       ┌──────────────┐
│   Category   │       │     User     │  (Django built-in)
│──────────────│       │──────────────│
│ id (UUID)    │       │ id           │
│ name         │       │ email        │
│ slug         │       │ username     │
│ description  │       └──────┬───────┘
└──────┬───────┘              │
       │  FK                  │ OneToOne        FK
       │              ┌───────▼───────┐    ┌───▼────────────┐
┌──────▼───────┐      │     Cart      │    │    Order       │
│   Product    │      │───────────────│    │────────────────│
│──────────────│      │ id (UUID)     │    │ id (UUID)      │
│ id (UUID)    │      │ user (FK/null)│    │ user (FK)      │
│ category(FK) │      │ session_key   │    │ status         │
│ name         │      └───────┬───────┘    │ first_name     │
│ slug         │              │            │ last_name      │
│ price        │         FK (items)        │ email          │
│ stock        │              │            │ address_line_1 │
│ is_active    │      ┌───────▼───────┐    │ city / state   │
└──────┬───────┘      │   CartItem    │    │ subtotal       │
       │              │───────────────│    │ shipping_cost  │
       │    FK        │ id (UUID)     │    │ total          │
       └──────────────│ cart (FK)     │    └───────┬────────┘
                      │ product (FK)  │            │
                      │ quantity      │       FK (items)
                      └───────────────┘            │
                                           ┌───────▼────────┐
                                           │   OrderItem    │
                                           │────────────────│
                                           │ id (UUID)      │
                                           │ order (FK)     │
                                           │ product (FK)   │
                                           │ product_name ◄─┼─ snapshot
                                           │ unit_price   ◄─┼─ snapshot
                                           │ quantity       │
                                           └────────────────┘
```

**Decisiones de diseño notables:**

- Todos los modelos usan **UUID como PK** (evita exponer conteos internos en URLs)
- `Cart` soporta dueño anónimo (`session_key`) o autenticado (`user`) mutuamente excluyentes mediante `CheckConstraint`
- `OrderItem` guarda `product_name` y `unit_price` como **snapshot**: si el precio del producto cambia después de la compra, el historial de órdenes permanece correcto

---

## 9. Flujo de la aplicación

### 9.1 Agregar al carrito

```
Usuario hace POST /cart/add/<product_id>/
    │
    ▼
AddToCartView.post()
    │  delega a
    ▼
CartService.add_item(request, product_id, quantity)
    ├── ProductRepository.get_by_id()      → valida existencia
    ├── CartService.get_or_create_cart()   → resuelve carrito (user o sesión)
    ├── CartItemRepository.get_by_cart_and_product() → busca item existente
    ├── product.has_sufficient_stock()     → regla de negocio
    └── CartItemRepository.save()          → persiste
    │
    ▼
Redirect con mensaje de éxito / error
```

### 9.2 Proceso de checkout

```
GET /checkout/  →  CheckoutView muestra formulario con resumen del carrito
    │
    ▼
Usuario llena datos de envío y hace POST /checkout/
    │
    ▼
CheckoutView.post()
    ├── CheckoutForm.is_valid()            → validación del formulario
    └── CheckoutService.place_order()
            │
            ├── 1. Validar que el carrito no esté vacío
            ├── 2. OrderFactory.build()    → crear instancia de Order
            ├── 3. OrderRepository.save()  → persistir la orden
            ├── 4. OrderFactory.build_items() → crear OrderItems (con snapshot)
            ├── 5. CartItemRepository.save() → persistir cada línea
            ├── 6. Product.stock -= quantity  → decrementar stock (select_for_update)
            ├── 7. PaymentStrategy.process() → cobrar (DummyStrategy en demo)
            ├── 8. order.status = CONFIRMED  → confirmar orden
            └── 9. CartService.clear_cart()  → vaciar carrito
    │
    ▼
Redirect a /checkout/confirmation/<order_id>/
```

---

## 10. Protección de URLs y seguridad

### Protección por autenticación

| URL | Protección | Mecanismo |
|---|---|---|
| `/products/` | Pública | Ninguna |
| `/cart/` | Pública | Sesión anónima disponible |
| `/checkout/` | **Login requerido** | `LoginRequiredMixin` |
| `/checkout/orders/` | **Login requerido** | `LoginRequiredMixin` |
| `/checkout/orders/<id>/` | **Login requerido** | `LoginRequiredMixin` + filtro por `user` |
| `/admin/` | Staff only | Django Admin |

### Protección a nivel de objeto

Las vistas de detalle de orden filtran explícitamente por el usuario actual, evitando que un usuario autenticado acceda a órdenes de otro usuario:

```python
# checkout/views.py
order = get_object_or_404(
    Order,
    pk=order_id,
    user=request.user,  # ← object-level permission
)
```

### Otras medidas de seguridad

- **CSRF tokens** en todos los formularios POST
- **`select_for_update()`** al decrementar stock, evitando race conditions en compras concurrentes
- **UUIDs como PKs** en todas las entidades, haciendo impredecibles los IDs de órdenes en URLs
- **Snapshot de precios** en `OrderItem`, evitando manipulación de precios post-compra

---

## 11. Instalación y ejecución

### Requisitos

- Python 3.10+
- pip

### Pasos

```bash
# 1. Entrar a la carpeta del proyecto (importante)
cd basic_checkout

# 2. Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 5. Crear superusuario (para acceder al admin)
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver
```

### URLs disponibles

| URL | Descripción |
|---|---|
| `http://127.0.0.1:8000/` | Redirige al catálogo |
| `http://127.0.0.1:8000/products/` | Catálogo de productos |
| `http://127.0.0.1:8000/cart/` | Carrito de compras |
| `http://127.0.0.1:8000/checkout/` | Proceso de pago |
| `http://127.0.0.1:8000/accounts/login/` | Inicio de sesión |
| `http://127.0.0.1:8000/accounts/signup/` | Registro |
| `http://127.0.0.1:8000/admin/` | Panel de administración |

### Agregar productos de prueba

Desde el panel de administración (`/admin/`) se pueden crear categorías y productos. El sistema requiere al menos un producto con `stock > 0` e `is_active = True` para que aparezca en el catálogo.

---

## Notas finales

Este proyecto fue desarrollado con el objetivo de producir **código limpio, bien estructurado y académicamente riguroso**, priorizando la claridad arquitectónica sobre la completitud de funcionalidades. Cada decisión de diseño puede trazarse directamente a un principio SOLID o a un patrón de diseño documentado.

> *"Programs must be written for people to read, and only incidentally for machines to execute."*  
> — Harold Abelson
