'''
Crear una clase que represente  una cuenta bancaria, sobre una cuenta se pueden realizar las siguientes operaciones:

1.- Abrir una cuenta
2.- Depositar Dinero
3.- Retitar Dinero
4.- Consultar Saldo
5.- Cerrar Cuenta

Se deben incluir atributos (propiedades o caracteristicas) como:

1.- Nombre del Cliente
2.- Número de la Cuenta
3.- Saldo
4.- Estado (activo o inactivo)
'''

class CuentaBancaria(object):

    def __init__(self, numero, cliente, saldo=1000, estado=True) -> None:
        self.numero = numero
        self.cliente = cliente
        self.saldo = saldo
        self.estado = estado

    def depositar(self, cantidad):
        if self.estado and cantidad > 0:
            self.saldo += cantidad 

    def retirar(self, cantidad):
        if self.estado and  cantidad > 0 and cantidad <= self.saldo: 
            self.saldo-= cantidad           

    def cerrar_cuenta(self):         
        self.estado = False

    def __str__(self) -> str:
        return f'{self.numero};{self.cliente}; {self.saldo};{self.estado}'

# crear un objeto de tipo cuentaBancaria

cuenta_ahorros = CuentaBancaria(12345,'JOse Perez', saldo=50000)

print(cuenta_ahorros.cliente)
print(cuenta_ahorros.saldo)
cuenta_ahorros.depositar(10000)
print(cuenta_ahorros.saldo)
cuenta_ahorros.retirar(20000)
print(cuenta_ahorros.saldo)

#crear un objeto de tipo cuentaBancaria transferencia

cuenta_corriente = CuentaBancaria(67890, 'Angela Burgos', 100000)

retirarEfectivo = 20000

cuenta_corriente.retirar(retirarEfectivo)
print(cuenta_corriente.saldo)

#transferir 

print(cuenta_ahorros.saldo)
cuenta_ahorros.depositar(retirarEfectivo)
print(cuenta_ahorros.saldo)

#mover todo el dinero a cuenta ahorros

dinero = cuenta_corriente.saldo

cuenta_ahorros.depositar(dinero)
print(cuenta_ahorros.saldo)
print(cuenta_corriente.saldo)

#cerrar cuenta

cuenta_corriente.cerrar_cuenta()
print(cuenta_corriente.estado)




print(cuenta_corriente)