classDiagram
    %% CONTRATOS Y CLASES BASE
    class Exportable {
        <>
        +exportar() str
    }

    class Figura {
        #_nombre: str
        #_color: str
        #_construida: bool
        +area() float
    }

    class Poligono {
        <>
        #_lados: list
        #_observaciones: list
        +lados_esperados()* int
        +perimetro() float
        +agregar_observacion(texto: str)
        +exportar() str
        +lados() tuple
    }

    %% HERENCIA DE DOMINIO (Las figuras concretas)
    Figura <|-- Poligono
    Poligono <|-- Triangulo
    Poligono <|-- Cuadrado
    Poligono <|-- Pentagono
    Poligono <|-- Hexagono

    %% EL REDISEÑO (Duck Typing y Clases Independientes)
    class PoligonoRegular {
        -nombre: str
        -color: str
        -_cantidad: int
        -_lados: list
        +perimetro() float
        +lados() tuple
    }

    class PlanoCAD {
        <>
        -identificador: str
        +exportar() str
    }

    %% REALIZACIÓN DEL PROTOCOLO (Implementación estructural)
    Exportable <|.. Poligono : cumple contrato
    Exportable <|.. PlanoCAD : cumple contrato

    %% COMPOSICIÓN, AGREGACIÓN Y ASOCIACIÓN (Las Partes)
    class Taller {
        -_poligonos: list
        +recibir(poligono: Poligono)
        +restaurar(poligono: Poligono)
        +inventario() tuple
    }

    class Lado {
        -_longitud: float
        -_etiqueta: Etiqueta
        +longitud() float
        +escalar(factor: float)
    }

    class Etiqueta {
        <>
        +texto: str
    }

    %% RELACIONES ESTRUCTURALES
    Taller o-- Poligono : Agregación
    Poligono *-- Lado : Composición
    PoligonoRegular *-- Lado : Composición
    Lado --> "0..1" Etiqueta : Asociación