"""
demo_sintomas.py

Este script demuestra los problemas de memoria y ciclo de vida generados por 
dos de los java-ismos encontrados en la Parte 1 antes de ser corregidos.
"""

print("--- SÍNTOMA 1: El default mutable (Argumento []) ---")

class PoligonoDefaultMutable:
    # Java-ismo: usar [] como valor por defecto
    def __init__(self, nombre, observaciones=[]):
        self.nombre = nombre
        self._observaciones = observaciones

# Instanciamos dos polígonos distintos, sin pasarles observaciones
p1 = PoligonoDefaultMutable("Triángulo")
p2 = PoligonoDefaultMutable("Cuadrado")

# Le agregamos una observación solo al primero
p1._observaciones.append("Falta pintar")

print(f"Observaciones del {p1.nombre}: {p1._observaciones}")
# El síntoma: el segundo polígono también tiene la observación
print(f"Observaciones del {p2.nombre}: {p2._observaciones}")
# Comprobación de que son la misma lista exacta en memoria 
print(f"¿Comparten la misma lista en memoria?: {p1._observaciones is p2._observaciones}\n")


print("--- SÍNTOMA 2: El 'static' accidental (Atributo de clase) ---")

class PoligonoStaticAccidental:
    # Java-ismo: variable declarada fuera del __init__
    catalogo = []
    
    def __init__(self, nombre):
        self.nombre = nombre
        PoligonoStaticAccidental.catalogo.append(self)

# Instanciamos dos polígonos
poly1 = PoligonoStaticAccidental("Hexágono")
poly2 = PoligonoStaticAccidental("Pentágono")

# El síntoma: ambos objetos ven el mismo catálogo 
print(f"Catálogo visto desde poly1: {[p.nombre for p in poly1.catalogo]}")
print(f"Catálogo visto desde poly2: {[p.nombre for p in poly2.catalogo]}")
print(f"¿Ambos apuntan a la misma variable estática?: {poly1.catalogo is poly2.catalogo}")