from typing import override


class Figura:
    def __init__(self, nombre, color):
        self._nombre = nombre
        self._color = color
        self._construida = True

    def area(self) -> float:
        return 0.0


class Lado:
    def __init__(self, longitud):
        self.longitud = longitud

    @property
    def longitud(self):
        return self._longitud

    @longitud.setter
    def longitud(self, valor):
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor


class Poligono(Figura):
    def __init__(self, nombre, color, lados=None, observaciones=None):
        super().__init__(nombre, color)
        
        self._lados = lados if lados is not None else []
        self._observaciones = observaciones if observaciones is not None else []

    @property
    def lados(self):
        return tuple(self._lados)

    def lados_esperados(self):
        return 0

    def perimetro(self):
        return sum(l.longitud for l in self._lados)

    def agregar_observacion(self, texto):
        self._observaciones.append(texto)

    @override
    def area(self) -> float:
        return 0.0


class Triangulo(Poligono):
    def __init__(self, lados=None):
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


class PoligonoRegular(Poligono):
    def __init__(self, nombre, color, medida, cantidad):
        super().__init__(nombre, color, [Lado(medida) for _ in range(cantidad)])
        self._cantidad = cantidad

    @override
    def lados_esperados(self):
        return self._cantidad


if __name__ == "__main__":
    activo = True
    if activo:                                      
        t = Triangulo([Lado(3), Lado(4), Lado(5)])
        c = Cuadrado([Lado(2), Lado(2), Lado(2), Lado(2)])
        
        print(f"Perímetro del triángulo: {t.perimetro()}")      
        print(f"Perímetro del cuadrado: {c.perimetro()}")
        
        t.agregar_observacion("revisar el vértice A")
        print(f"Nombre: {t._nombre}")
        
        r = PoligonoRegular("Pentágono", "verde", 4, 5)
        print(f"Perímetro del pentágono: {r.perimetro()}")