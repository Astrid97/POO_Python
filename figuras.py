from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, override


# --- CONTRATO ESTRUCTURAL ---
class Exportable(Protocol):
    def exportar(self) -> str:
        ... # Los tres puntos son válidos en Python para indicar que está vacío

class Figura:
    def __init__(self, nombre, color):
        self._nombre = nombre
        self._color = color
        self._construida = True   # marca de que Figura.__init__ realmente corrió

    def area(self) -> float:
        return 0.0

@dataclass(frozen=True)
class Etiqueta:
    """Implementada como dataclass inmutable"""
    texto: str

class Lado:
    #Asociacion(0..1): un lado puede tener una etiqueta, pero no es obligatorio
    def __init__(self, longitud, etiqueta: Etiqueta | None = None):
        self._longitud = longitud
        self._etiqueta = etiqueta

    @property
    def longitud(self):
        return self._longitud

    @longitud.setter
    def longitud(self, valor):
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor
    
    # metodo pedido por el diagrama
    def escalar(self, factor):
        self._longitud *= factor
    

class Poligono(Figura, ABC):

    def __init__(self, nombre, color, lados=None, observaciones=None):
        # Llamada a super() como primera linea (Java-ismo resuelto)
        super().__init__(nombre, color)
        
        # Default mutable arguments (Java-ismo resuelto)
        self._lados = lados if lados is not None else []
        self._observaciones = observaciones if observaciones is not None else []
        
        #Validación de cantidad de lados 
        if self._lados and len(self._lados) != self.lados_esperados():
            raise ValueError(f"Se esperaban {self.lados_esperados()} lados, pero se recibieron {len(self._lados)}")
   
   
    # Copiar la lista de lados en lugar de exponerla directamente (Java-ismo resuelto)
    @property
    def lados(self):
        return tuple(self._lados)  # devuelve una tupla inmutable de los lados

    @abstractmethod
    def lados_esperados(self) -> int:
        pass

    def perimetro(self):
        # Bucle manual reemplazado por comprensión de lista y sum() (Java-ismo resuelto)
        return sum(l.longitud for l in self._lados)

    def agregar_observacion(self, texto):
        self._observaciones.append(texto)
        
    # Type hint corregido y el @override agregado (Java-ismo resuelto)
    @override
    def area(self) -> float:
        return 0.0
    
    def exportar(self) -> str:
        return f"Poligono: {self._nombre} ({self.lados_esperados()} lados)"

class Triangulo(Poligono):
    def __init__(self, lados=None):
        # Sobrecarga simulada resuelta, un solo constructor simple (Java-ismo resuelto)
        super().__init__("triángulo", "negro", lados)

    @override
    def lados_esperados(self):
        return 3


class Cuadrado(Poligono):
    def __init__(self, lados=None):
        super().__init__("cuadrado", "negro", lados)

    @override
    def lados_esperados(self):
        return 4

# Clases nuevas exigidas
class Pentagono(Poligono):
    def __init__(self, lados=None):
        super().__init__("pentágono", "verde", lados)

    @override
    def lados_esperados(self):
        return 5
    
class Hexagono(Poligono):
    def __init__(self, lados=None):
        super().__init__("hexágono", "amarillo", lados)

    @override
    def lados_esperados(self):
        return 6
    
#Resideño: Poligonoregular ya no hereda de Poligono
class PoligonoRegular:
    """Polígono de N lados de igual longitud."""
    def __init__(self, nombre, color, medida, cantidad):
        self.nombre = nombre
        self.color = color
        #Composicion: fabrica sus propios lados adentro 
        self._lados = [Lado(medida) for _ in range(cantidad)]
        self._cantidad = cantidad
        
    def perimetro(self):
        return sum(l.longitud for l in self._lados)
    
    @property
    def lados(self):
        return tuple(self._lados) 


class Taller:
    def __init__(self):
        self._poligonos = [] # inicia vacio
    
    def recibir(self, poligono: Poligono):
        #Agregacion: el taller recibe un polígono, pero no es dueño de él
        self._poligonos.append(poligono)
    
    def restaurar(self, poligono: Poligono):
        pass  # implementación pendiente
    
    def inventario(self) -> tuple[Poligono, ...]:
        return tuple(self._poligonos)  # devuelve una tupla inmutable de los polígonos



def exportar_todo(items: list[Exportable]) -> list[str]:
    # Gracias al Protocol, Python sabe que todo lo que entre acá tendrá un .exportar()
    return [item.exportar() for item in items]