# Trabajo Práctico - Programación Orientada a Objetos (UTN)
**Alumna:** Astrid Añazco

Este repositorio contiene la entrega final del TP de refactorización y diseño orientado a objetos (de Java a Python). A continuación se detalla la responsabilidad y el contenido de cada archivo incluido en la carpeta raíz:

### Archivos de Código
* **`figuras.py`**: Contiene el modelo de dominio completo y rediseñado (Partes 1 a 4). Incluye la clase abstracta `Poligono`, el rediseño de `PoligonoRegular` como clase independiente, las implementaciones de las relaciones estructurales (Composición en Lados, Agregación en `Taller`, Asociación en `Etiqueta`) y la definición del contrato estructural `Exportable` mediante `Protocol`.
* **`parte1_diagnostico.py`**: Es el archivo base provisto por la cátedra, después de haber solucionado exclusivamente los 8 "java-ismos" de sintaxis, pero conservando la herencia y arquitectura original.
* **`demo_sintomas.py`**: Script de demostración (Parte 1) que aísla y ejecuta dos de los errores originales (el default mutable `[]` y el static accidental). Utiliza el operador `is` para comprobar matemáticamente la falla en el manejo de memoria de las instancias compartidas.
* **`libreria_externa.py`**: Módulo simulado de un SDK de terceros (contiene `PlanoCAD`). Se incluye en la entrega **sin modificar**, comprobando que el sistema puede acoplar objetos externos usando Duck Typing en lugar de forzar herencia.
* **`main.py`**: El script ejecutable final (Parte 5). Importa las clases del dominio, instancia el `Taller`, arma polígonos con etiquetas, integra el `PlanoCAD` y ejecuta la función polimórfica `exportar_todo()` para demostrar que el sistema completo funciona sin errores.

### Documentación
* **`informe.md`**: Documento teórico que responde a las consignas del trabajo (máximo 1 carilla). Incluye la tabla de diagnóstico de los 8 java-ismos, la tabla de equivalencias con el código final refactorizado, y las justificaciones arquitectónicas sobre el uso de relaciones, Duck Typing y Protocolos.
* **`uml/modelo_final.md`**: Contiene el código Mermaid puro que renderiza el diagrama de clases UML definitivo. Refleja las jerarquías actualizadas, la abstracción de `Poligono` y la independización de `PoligonoRegular`.