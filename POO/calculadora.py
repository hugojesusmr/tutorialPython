class Calculadora:
    def suma(self, num1, num2):
        return num1 + num2
    
    def resta(self, num1, num2):
        return num1 - num2
    
    def producto(self, num1, num2):
        return num1 * num2
    
    def division(self, num1, num2):
        return num1 / num2
    

#creando una instancia

calculadora_basica = Calculadora()
suma = calculadora_basica.suma(1,2)

print(f'La suma es: {suma}')
    
    