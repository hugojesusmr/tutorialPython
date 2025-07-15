class Vehiculo(object):
    '''Representa la clase base para una jerarquia de herencia vehiculos'''
    def __init__(self, placa, marca, modelo, pais) -> None:
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.pais = pais
        self.estado = False
        self.velocidad = 0
        
    def encender(self):
        if not self.estado:
            self.estado = True

    def apagar(self):
        if self.estado:
            self.estado = False

    def acelerar(self):
        if self.estado:
           self.velocidad += 2

    def frenar(self):
        if self.estado:
           self.velocidad = 0                             


class Camion(Vehiculo):
    '''Representa un Camion en la jerarquia de Vehiculos'''
    def __init__(self, placa, marca, modelo, pais, capacidad_carga) -> None:
        '''Crea un Nuevo Camión'''
        super().__init__(placa, marca, modelo, pais)
        self.capacidad_carga = capacidad_carga
        #Cuando se crea un camion la carga es 0
        self.carga_actual = 0 

    def carga_mercancia(self, cantidad):
        if self.carga_actual + cantidad <= self.capacidad_carga:
            self.capacidad_carga += cantidad    

    def descargar_mercancia(self):
        self.carga_actual = 0        