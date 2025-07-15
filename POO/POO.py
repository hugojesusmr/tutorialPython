
''' Introducción a la Programación Orientada a Objetos 

* EL Mundo Real o Natural esta compuesto de objetos o entidades que se pueden representar para la 
creación de aplicaciones de software

* La POO es una tecnica o tecnologia que permite simular la realidad con el fin de resolver problemas de una
manera mas exacta y eficiente.

Miembros de una Clase:

  * Campos de Instancia = representan el estado del objeto

  * Campos de Instancia Privados = Es una varible que solo es visible para el cuerpo de declaración de una clase.
        Esto apoya la encapsulación.
        -> El guion bajo representa un campo privado( _ ).

  * Métodos de Instancia = representan el comportamiento del objeto
     -> Los métodos tienen un parametro obligatorio = self
     -> Las funciones(métodos  de instancia): definen lo que el objeto (entidad) puede hacer que quiere decir (su comportamiento)

Palabra clave de Python:
  * self = significa que esta variable, metodo es un campo de instancia que pertenece a esa clase

  * @Property = Establecemos una propiedad para una clase  de objeto
 Encapsulación: Patrón de Diseño para definir los mibros que solo son visibles al interior de una entidad(clase)

 Lectura de POO

 1.- Abstracción

 2.- Herencia

 
 3.- Polimorfismo
 4.- Encapsulacion 
'''

class Persona:
    #dedfinicion del encabezzado de una función
    def __init__(self, documento, nombre_completo, email, direccion):
        #creando campos de instancia
        self.documento = documento
        self.nombre_completo = nombre_completo
        self.email = email
        self.direccion = direccion

    def caminar(self):
        print('La persona esta caminando')

    def trabajando(self):
        print('La persona esta trabajando')         

#  Instancia de un Objeto y Acceder a los Valores de Campos de Instancia

hugo = Persona(123456789,'Hugo de Jesus Melo rangel','hugi@mail.com','cocoyotes')

#Acceso a las propiedades de un objeto
print(hugo.documento)

#invocar funciones

hugo.caminar()