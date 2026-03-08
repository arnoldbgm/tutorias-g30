Claro, aquí va la guía actualizada sin encapsulamiento, enfocada en los 3 pilares restantes:

---

# 🛠️ Guía de Laboratorio: Programación Orientada a Objetos (POO) en Python

> 💡 **Duración:** 1 hora 30 minutos | **Nivel:** Básico | **Requisito:** Variables, condicionales, bucles

La POO te permite **modelar objetos del mundo real** dentro de un programa, agrupando datos y comportamientos en una estructura llamada **clase**.

---

## ⏱️ Distribución de la sesión

| Bloque | Tema | Tiempo |
|---|---|---|
| 1 | Clases, objetos y constructor | 30 min |
| 2 | Herencia | 30 min |
| 3 | Polimorfismo | 20 min |
| 4 | Proyecto final | 10 min |

---

# 🔹 BLOQUE 1 — Clases, Objetos y Constructor *(30 min)*

## ¿Qué es una clase?

Una **clase** es un molde para crear objetos. Así como un plano de una casa no es la casa, una clase no es el objeto — es la plantilla.

| Objeto real | Clase en código |
|---|---|
| Auto | `Auto` |
| Persona | `Persona` |
| Cuenta bancaria | `CuentaBancaria` |

Todo objeto tiene:
- **Atributos** → características (color, nombre, saldo)
- **Métodos** → acciones (acelerar, saludar, depositar)

## Crear una clase y un objeto

```python
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print(f"Hola, soy {self.nombre} y tengo {self.edad} años")


# Crear objetos
p1 = Persona("Ana", 22)
p2 = Persona("Luis", 30)

p1.saludar()
p2.saludar()
```

```
Hola, soy Ana y tengo 22 años
Hola, soy Luis y tengo 30 años
```

📌 **Puntos clave:**
- `__init__` es el **constructor**: se ejecuta automáticamente al crear el objeto
- `self` representa al **objeto actual** (siempre es el primer parámetro)
- Cada objeto tiene **sus propios valores** de atributos

## Ejemplo completo — Clase CuentaBancaria

```python
class CuentaBancaria:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, monto):
        self.saldo += monto
        print(f"Depósito exitoso. Saldo: {self.saldo}")

    def retirar(self, monto):
        if monto > self.saldo:
            print("Fondos insuficientes")
        else:
            self.saldo -= monto
            print(f"Retiro exitoso. Saldo: {self.saldo}")

    def mostrar_saldo(self):
        print(f"Titular: {self.titular} | Saldo: {self.saldo}")


cuenta = CuentaBancaria("María", 1000)
cuenta.depositar(500)
cuenta.retirar(200)
cuenta.mostrar_saldo()
```

```
Depósito exitoso. Saldo: 1500
Retiro exitoso. Saldo: 1300
Titular: María | Saldo: 1300
```

## 🧪 Ejercicio 1 — Clase Estudiante

Crea una clase `Estudiante` con atributos `nombre`, `carrera` y `nota`. Agrega un método `aprobo()` que imprima si el alumno aprobó (nota >= 60) o reprobó.

```
# Salida esperada:
Ana - Ingeniería → Aprobó
Luis - Medicina → Reprobó
```

## 🧪 Ejercicio 2 — Clase Producto

Crea una clase `Producto` con atributos `nombre`, `precio` y `stock`. Agrega:
- `mostrar_info()` → muestra todos los datos
- `vender(cantidad)` → descuenta del stock solo si hay suficiente, si no muestra `"Stock insuficiente"`

---

# 🔹 BLOQUE 2 — Herencia *(30 min)*

## ¿Qué es la herencia?

La herencia permite crear una clase **nueva basada en otra existente**. La clase hija hereda todos los atributos y métodos de la clase padre, y puede agregar los suyos propios.

```
        Animal
       /      \
    Perro     Gato
```

```python
# Clase padre
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre

    def comer(self):
        print(f"{self.nombre} está comiendo")

    def hacer_sonido(self):
        print("Sonido genérico")


# Clases hijas
class Perro(Animal):
    def hacer_sonido(self):
        print(f"{self.nombre} dice: ¡Guau!")

    def buscar_pelota(self):
        print(f"{self.nombre} busca la pelota")


class Gato(Animal):
    def hacer_sonido(self):
        print(f"{self.nombre} dice: ¡Miau!")


perro = Perro("Rex")
gato = Gato("Misi")

perro.comer()           # heredado de Animal
perro.hacer_sonido()    # sobreescrito en Perro
perro.buscar_pelota()   # propio de Perro
gato.hacer_sonido()
```

```
Rex está comiendo
Rex dice: ¡Guau!
Rex busca la pelota
Misi dice: ¡Miau!
```

## Usar `super()` para extender el constructor

Cuando la clase hija necesita **sus propios atributos además de los del padre**, se usa `super()`.

```python
class Empleado:
    def __init__(self, nombre, sueldo):
        self.nombre = nombre
        self.sueldo = sueldo

    def mostrar_info(self):
        print(f"Nombre: {self.nombre} | Sueldo: {self.sueldo}")


class Gerente(Empleado):
    def __init__(self, nombre, sueldo, departamento):
        super().__init__(nombre, sueldo)    # llama al constructor del padre
        self.departamento = departamento

    def mostrar_info(self):
        print(f"Nombre: {self.nombre} | Depto: {self.departamento} | Sueldo: {self.sueldo}")


e = Empleado("Juan", 3000)
g = Gerente("Carlos", 8000, "Tecnología")

e.mostrar_info()
g.mostrar_info()
```

```
Nombre: Juan | Sueldo: 3000
Nombre: Carlos | Depto: Tecnología | Sueldo: 8000
```

📌 **Puntos clave:**
- `class Hija(Padre)` → sintaxis de herencia
- `super()` → accede al constructor del padre sin repetir código
- La hija **hereda todo** y puede **agregar o sobreescribir** lo que necesite

## 🧪 Ejercicio 3 — Sistema de Empleados

Crea una clase `Empleado` con `nombre` y `sueldo`. Luego crea dos clases hijas:
- `Desarrollador` con atributo `lenguaje` y método `programar()`
- `Vendedor` con atributo `region` y método `vender()`

Ambas deben tener `mostrar_info()` que imprima todos sus datos.

```
# Salida esperada:
Desarrollador: Ana | Lenguaje: Python | Sueldo: 4000
Ana está programando en Python

Vendedor: Luis | Región: Norte | Sueldo: 3500
Luis está vendiendo en la región Norte
```

---

# 🔹 BLOQUE 3 — Polimorfismo *(20 min)*

## ¿Qué es el polimorfismo?

Polimorfismo significa que **objetos diferentes pueden responder al mismo método** de formas distintas. "Mismo mensaje, distinta respuesta."

```python
class Figura:
    def area(self):
        pass

class Rectangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura

class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return 3.1416 * self.radio ** 2

class Triangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return (self.base * self.altura) / 2


# Polimorfismo en acción: mismo método, objetos distintos
figuras = [
    Rectangulo(5, 3),
    Circulo(4),
    Triangulo(6, 2)
]

for figura in figuras:
    print(f"Área: {figura.area():.2f}")
```

```
Área: 15.00
Área: 50.27
Área: 6.00
```

📌 **Puntos clave:**
- El mismo método `area()` produce resultados distintos según el objeto
- Permite escribir código general que funciona con **cualquier tipo de figura**
- Es la base de sistemas escalables y flexibles

## 🧪 Ejercicio 4 — Sistema de Pagos

Crea una clase base `MetodoPago` con un método `pagar(monto)`. Luego crea tres clases hijas:
- `Efectivo` → imprime `"Pagando $X en efectivo"`
- `TarjetaCredito` → imprime `"Cargando $X a tarjeta de crédito"`
- `PayPal` → imprime `"Enviando $X por PayPal"`

Recorre una lista con los tres métodos y llama `pagar(500)` en cada uno.

```
# Salida esperada:
Pagando $500 en efectivo
Cargando $500 a tarjeta de crédito
Enviando $500 por PayPal
```

---

# 🎯 PROYECTO FINAL *(10 min)* — Sistema de Tienda

Integra todo lo aprendido en un solo programa:

```
Clase base:     Producto  (nombre, precio, stock)
Clases hijas:   ProductoFisico  (peso)
                ProductoDigital (link_descarga)
```

**Requisitos:**
- Ambas clases hijas deben usar `super()` en su constructor
- Ambas deben tener `mostrar_info()` con salida diferente
- Ambas deben heredar y usar el método `vender(cantidad)` del padre
- Crea al menos 2 objetos de cada tipo y recórrelos en una lista llamando `mostrar_info()`

---

# 📊 Resumen

| Pilar | ¿Qué hace? | Clave en Python |
|---|---|---|
| **Clases y Objetos** | Estructura el código en moldes reutilizables | `class`, `__init__`, `self` |
| **Herencia** | Reutiliza código entre clases relacionadas | `class Hija(Padre)`, `super()` |
| **Polimorfismo** | Mismo método, comportamiento distinto | Sobreescritura de métodos |

