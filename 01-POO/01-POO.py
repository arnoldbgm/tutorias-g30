# Programacion Orientada a Objetos
# ES una pardigma de programacion 
# (es una forma de trabjaar o programar)
# Se trabaja usando clases y objetos

# class Persona:
#     # Constructor => Es el metodo especial
#     # Donde detallamos las caracteristicas
#     # atributos de nuestra clase
#     def __init__(self, nombre, edad, apellido):
#         self.nombre = nombre
#         self.edad = edad
#         self.apellido = apellido

#     def saludar(self):
#         print(f"Hola, soy {self.nombre} y tengo {self.edad} años")
   
#     def despedida(self):
#         print(f"Adios, soy {self.nombre}")


# # Crear objetos
# p2 = Persona("Ramon", 30, "Perez")
# p3 = Persona("Maria", 25, "Gomez")

# p2.despedida()

# p3.saludar()


### 🏦 Banco
## Crear una clase de un Banco para sus cuentas bancarias
#  con las siguientes caracteristicas:
#  Titular
#  Saldo

# class CuentaBancaria:

#    def __init__(self, titular, saldo, comision):
#       self.titular = titular
#       self.saldo = saldo
#       self.comision = comision

#    # Metodo => funcion => accion
#    # Metodo para depositar - retirar - consultar el saldo
#    def consultar_saldo(self):
#       print(f"Tu saldo es {self.saldo}")

#    def depositar(self, cantidad_ingresada):
#       self.saldo = self.saldo + cantidad_ingresada

#    def retirar(self, cantidad_retirar):
#       # Validacion => No podemos retirar si el monto es mayor
#       # al saldo
#       if cantidad_retirar > self.saldo:
#          print("No puedes retirar")
#       else:
#          self.saldo = (self.saldo - cantidad_retirar) - self.comision
# # Instanciar => Crear un objeto => Pasar la masa por el molde

# c1 = CuentaBancaria("Ramon", 2500)
# c1.consultar_saldo()

# c1.depositar(300)

# c1.consultar_saldo()

# c1.retirar(5000)

# c1.consultar_saldo()

# Clase padre
# class Animal:
#     def __init__(self, nombre):
#         self.nombre = nombre

#     def comer(self):
#         print(f"{self.nombre} está comiendo")

#     def hacer_sonido(self):
#         print("Sonido genérico")


# # Clases hijas
# class Perro(Animal):
#     def __init__(self, nombre, raza, color):
#         # Aqui usamos el metodo super para llamar
#         # al constructor de la clase padre
#         super().__init__(nombre)
#         # Nuevos atributos de la clase hija
#         self.raza = raza
#         self.color = color

#     def hacer_sonido(self):
#         print(f"{self.nombre} dice: ¡Guau!")

#     def buscar_pelota(self):
#         print(f"{self.nombre} busca la pelota")

#     def dar_la_pata(self):
#         print(f"{self.nombre} da la pata")

# firulais = Perro("Firulais")
# firulais.hacer_sonido()



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

# Polimorfismo => Es una clase con multiples formas
e1 = Empleado("Miguel", 4000)
e2 = Empleado("Maria", 5000)
e3 = Empleado("Raquel", 8000)

# g = Gerente("Carlos", 8000, "Tecnología")

e1.mostrar_info()
e2.mostrar_info()
e3.mostrar_info()