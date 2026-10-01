from figuras import (
    Cuadrado,
    Etiqueta,
    Hexagono,
    Lado,
    PoligonoRegular,
    Taller,
    Triangulo,
    exportar_todo,
)
from libreria_externa import PlanoCAD


def main():
    print("=== INICIANDO SISTEMA GEOMÉTRICO ===\n")
    
    # 1. Instanciamos el Taller (El contenedor principal)
    mi_taller = Taller()

    # 2. Creamos las Etiquetas (Dataclasses inmutables)
    etiqueta_base = Etiqueta("Base de soporte principal")
    etiqueta_lateral = Etiqueta("Pared lateral")

    # 3. Armamos las figuras (El "Todo") componiendo sus Lados (Las "Partes")
    # Al triángulo le ponemos una etiqueta en la base
    t = Triangulo([Lado(5, etiqueta_base), Lado(4), Lado(4)])
    
    # Al cuadrado le ponemos una etiqueta en un lateral
    c = Cuadrado([Lado(2), Lado(2, etiqueta_lateral), Lado(2), Lado(2)])
    
    # Un hexágono sin etiquetas
    h = Hexagono([Lado(3), Lado(3), Lado(3), Lado(3), Lado(3), Lado(3)])

    # 4. El Taller recibe los polígonos (Agregación)
    mi_taller.recibir(t)
    mi_taller.recibir(c)
    mi_taller.recibir(h)

    # 5. Demostramos el rediseño de PoligonoRegular (Duck Typing)
    r = PoligonoRegular("Octógono", "morado", 10, 8)
    print(f"Demostracion: el {r.nombre} calcula su perímetro ({r.perimetro()}) sin heredar de Poligono.\n")

    # 6. Instanciamos el objeto de la librería de terceros
    plano = PlanoCAD("Plano_Principal") 

    # 7. Agrupamos todo lo que cumple el contrato Exportable (Protocol)
    # Extraemos la tupla del inventario, la pasamos a lista y le sumamos el plano
    elementos_a_exportar = list(mi_taller.inventario())
    elementos_a_exportar.append(plano)

# Comprobación visual de que la etiqueta existe en el lado 0 del triángulo
    print(f"La etiqueta del triángulo dice: {t.lados[0]._etiqueta.texto}\n")
    
    print("=== RESULTADOS DE LA EXPORTACIÓN ===")
    
    
    # 8. Ejecutamos la función 
    resultados = exportar_todo(elementos_a_exportar)
    
    for linea in resultados:
        print(linea)

if __name__ == "__main__":
    main()