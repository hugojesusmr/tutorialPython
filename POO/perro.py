class Perro(object):
    '''Representa la entidad Perro'''
    def __init__(self, nombre, edad, dueño) -> None:
        ''' Inicializa o instancia un nuevo objeto de la clase Perro'''
        self._nombre = nombre
        self._edad = edad
        self._dueño = dueño
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre
        

toby = Perro('toby',5, 'yo')

print(toby.get_nombre())