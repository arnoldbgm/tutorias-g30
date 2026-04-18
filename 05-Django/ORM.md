## Django ORM 🐍

### ¿Qué es el ORM?
El ORM (Object Relational Mapper) de Django permite trabajar con la base de datos usando **Python en lugar de SQL**.  
Es decir, en vez de escribir `SELECT * FROM tabla`, usamos objetos y métodos.

---

### 1. Crear un modelo (tabla en la base de datos)
Los modelos representan tablas en la base de datos.

```py
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
````

---

### 2. Crear y aplicar migraciones

Las migraciones crean las tablas en la base de datos.

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 3. Insertar datos (CREATE)

Crear registros en la base de datos:

```py
from .models import Categoria

# Forma 1
categoria = Categoria(nombre="Tecnología")
categoria.save()

# Forma 2 (más directa)
Categoria.objects.create(nombre="Deportes")
```

---

### 4. Obtener datos (READ)

Consultar información de la base de datos:

```py
# Obtener todos los registros
categorias = Categoria.objects.all()

# Obtener un solo registro
categoria = Categoria.objects.get(id=1)

# Filtrar datos
categorias = Categoria.objects.filter(nombre="Tecnología")
```

---

### 5. Actualizar datos (UPDATE)

Modificar registros existentes:

```py
categoria = Categoria.objects.get(id=1)
categoria.nombre = "Ciencia"
categoria.save()
```

---

### 6. Eliminar datos (DELETE)

Eliminar registros:

```py
categoria = Categoria.objects.get(id=1)
categoria.delete()
```

---

### 7. Consultas útiles

Algunos métodos comunes del ORM:

```py
# Obtener el primero
Categoria.objects.first()

# Obtener el último
Categoria.objects.last()

# Contar registros
Categoria.objects.count()

# Verificar si existe
Categoria.objects.filter(nombre="Tecnología").exists()
```

---

### 8. Ordenar resultados

```py
# Ascendente
Categoria.objects.all().order_by("nombre")

# Descendente
Categoria.objects.all().order_by("-nombre")
```

---

### 9. Limitar resultados

```py
# Obtener los primeros 5
Categoria.objects.all()[:5]
```

---

### 10. Buenas prácticas 🧠

* Usa nombres claros en modelos y campos
* Evita consultas innecesarias dentro de loops
* Usa `filter()` en vez de `get()` si no estás seguro de que existe
* Aprovecha el ORM antes de escribir SQL manual

---

💡 **Resumen rápido:**

* `create()` → crear datos
* `all()` → obtener todo
* `get()` → obtener uno
* `filter()` → filtrar
* `save()` → guardar cambios
* `delete()` → eliminar


