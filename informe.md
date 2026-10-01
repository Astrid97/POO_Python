# Parte 1 - Diagnóstico de java-ismos

| # | Java-ismo | Dónde (clase.método) | Inversión que lo explica | Síntoma observable |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Getters preventivos (y setters estilo Java Bean) | `Figura.getNombre`, `Figura.getColor`, `Lado.setLongitud` | En Java añadimos getters por las dudas para no romper todo en el futuro al agregar validaciones. En Python esto sobra, porque si un día necesito lógica, agrego `@property` y el que usa la clase ni se entera porque la sintaxis no cambia. | El código se llena de llamadas ruidosas con paréntesis que no sirven como `t.getNombre()` o `l.setLongitud(5)` en vez de acceder directo al atributo. |
| 2 | Atributo "static" accidental | `Poligono` (línea `catalogo = []`) | En Java es normal declarar las variables arriba de todo. En Python, si declarás algo directo bajo el `class` y fuera del `__init__`, se vuelve una variable estática de clase, compartida por todos los objetos. | Todos los polígonos instanciados terminan compartiendo y modificando la misma lista `catalogo` global en la memoria. |
| 3 | Argumento por defecto mutable | `Poligono.__init__` (parámetros `lados=[]`, `observaciones=[]`) | Uno cree que poner `[]` como default crea una lista nueva cada vez que llamás al constructor, pero Python lee y evalúa ese default una sola vez al cargar el archivo. | Si creo dos polígonos vacíos, los dos terminan apuntando a exactamente la misma lista en memoria. |
| 4 | `super().__init__()` olvidado | `Poligono.__init__` | El compilador de Java mete el llamado a `super()` de forma invisible si me lo olvido. En Python no: si no lo pongo como primera línea, el padre no se construye. | Se reasignan variables a mano y el objeto nace a medio hacer, porque los atributos originales de `Figura` (como `_construida`) nunca llegan a inicializarse. |
| 5 | Falta de copia defensiva (El oculto) | `Poligono.getLados` y `Poligono.__init__` | En Java pensamos que la lista está segura por ser `private`. En Python, si guardo el alias o devuelvo la lista original con un return, cualquiera de afuera le hace un `.append()` y corrompe el objeto. La solución es devolver una copia. | Si alguien hace `lista = p.getLados()`, le agrega un elemento y mágicamente el polígono tiene un lado más sin pasar por las validaciones. |
| 6 | Bucle acumulador manual | `Poligono.perimetro` | El clásico `for` de Java declarando un `total = 0` para ir sumando paso a paso. En Python se hace en una sola línea combinando `sum()` con listas por comprensión. | Código demasiado largo y "ruidoso" para resolver una operación matemática muy básica. |
| 7 | Sobrecarga de constructor simulada | `Triangulo.__init__`, `Cuadrado.__init__` | Como Python no deja escribir tres `__init__` con parámetros distintos, habia un montón de `if len(args)` y chequeos con `isinstance` para atajar todo en un solo lugar. | Termino con un constructor largo y difícil de leer, en lugar de armar métodos separados con `@classmethod`. |
| 8 | Type hint engañoso (y falso @Override) | `Poligono.area` | `-> int` para decir que devolvía un entero, pero termino devolviendo un string (`"area sin calcular"`). En Java el compilador avisa ese error; en Python si no usamos herramientas como `mypy`, los hints son de adorno. | El método devuelve texto aunque la firma promete un número entero, y el intérprete deja pasar el error silenciosamente. |


## Parte 2 - Pregunta Obligatoria (Relaciones Estructurales)

**Pregunta:** Si la sintaxis de guardar la referencia es idéntica en los tres casos (`self._algo=algo`), ¿cómo se ve en el código la diferencia entre agregación y composición?

**Respuesta:**
La diferencia no se ve en cómo se guarda el atributo, sino en el **ciclo de vida del objeto (quién lo fabrica y quién lo destruye)**. En el código, esto queda en evidencia al leer los constructores y las firmas de los métodos:

1. **Asociación (Lado -> Etiqueta):** La parte se recibe por parámetro de forma opcional. Son independientes.
   * *Línea que lo delata:* `def __init__(self, longitud, etiqueta: Etiqueta | None = None):` (La recibe desde afuera y admite `None`).
2. **Agregación (Taller -> Poligono):** El todo (Taller) no fabrica a las partes (Polígonos), las recibe ya instanciadas desde el exterior a través de un método. Las partes sobreviven si el todo desaparece.
   * *Línea que lo delata:* `def recibir(self, poligono: Poligono):` (El objeto entra por parámetro).
3. **Composición (Poligono -> Lado):** El todo fabrica a la parte internamente, atando sus ciclos de vida de forma permanente. 
   * *Línea que lo delata (en PoligonoRegular):* `[Lado(medida) for _ in range(cantidad)]` (El polígono instancia directamente a los lados en lugar de recibirlos armados).

## Parte 3 - Decisión sobre PoligonoRegular (Herencia vs. Duck Typing)

**Decisión:** Se decidió rediseñar `PoligonoRegular` quitándole la herencia (ya no hereda de `Poligono`), transformándola en una clase independiente. La jerarquía que se mantiene es la dictada por el dominio: las formas geométricas (`Triangulo`, `Cuadrado`, `Pentagono`, `Hexagono`).

**Justificación:** 
En Java, el programador original obligó a `PoligonoRegular` a heredar de `Poligono` por una pura "ceremonia del compilador": necesitaba un tipo padre compartido (`List`) para poder agruparlos a todos en el inventario del Taller. 

En Python, esa herencia sintáctica desaparece gracias al **Duck Typing**. Si queremos que `PoligonoRegular` conviva con los demás, no hace falta forzar un "es-un" que ensucie la taxonomía de nuestro dominio. Alcanza con que `PoligonoRegular` implemente los mismos métodos (como `perimetro()` y `@property lados`). Al hacerlo, cumple con el contrato estructural implícito y la clase `Taller` lo va a aceptar sin problemas en su método `recibir()`. Se eliminó una herencia artificial impuesta por el lenguaje, priorizando el diseño real.

## Parte 4 - ABC vs. Protocol

**1. Por qué una ABC no servía para PlanoCAD:**
Una clase abstracta (ABC) exige un contrato por herencia explícita: para cumplirlo, la clase está obligada a heredar de ella (`class PlanoCAD(Exportable):`). Como `PlanoCAD` es de un tercero y el archivo `figuras.py` no se puede modificar, es imposible forzar esa herencia. Un `Protocol` soluciona esto verificando el contrato de forma estructural (Duck Typing): no necesita que herede de nadie, le alcanza con ver que el objeto tenga el método `exportar()` en tiempo de ejecución.

**2. La elección entre ABC y Protocol, ¿la decide el lenguaje o el dominio?**
La decide estrictamente el dominio. 
Usamos una **ABC** cuando el modelo de negocio dicta una relación taxonómica «es-un» (ejemplo: un Triángulo *es un* Polígono). 
Usamos un **Protocol** cuando el dominio describe una capacidad transversal transversal o comportamiento. Un Polígono y un Plano CAD no comparten ninguna relación de familia biológica, pero ambos comparten la capacidad de ser *Exportables*. La herramienta no se elige por sintaxis de Python, sino por lo que representan los objetos en el mundo real.


## Tabla de equivalencias sobre el código

| Elemento en Java | Cómo quedó en tu código Python | ¿Traducción directa o rediseño? | Por qué |
| :--- | :--- | :--- | :--- |
| Interfaz `Exportable` explícita | `class Exportable(Protocol):` | Rediseño | En Java se exige herencia nominal para interfaces. En Python usamos un Protocolo para evaluar el comportamiento estructural (Duck Typing), permitiendo sumar a `PlanoCAD` sin tocar su código. |
| `class PoligonoRegular extends Poligono` | `class PoligonoRegular:` (independiente) | Rediseño | Java exigía heredar para meter la figura en un array compartido `List`. En Python no hace falta esta herencia; la lista acepta objetos distintos gracias al tipado dinámico. |
| `abstract class Poligono` | `class Poligono(Figura, ABC):` | Traducción directa | Ambos lenguajes comparten el concepto arquitectónico de Clase Abstracta para evitar la instanciación directa y forzar contratos lógicos (`@abstractmethod`). |
| Sobrecarga de constructores (ej. Triangulo) | Un solo `__init__` que llama a `super()` | Rediseño | Python no soporta sobrecarga de métodos nativa. Se resolvió el java-ismo inyectando los parámetros fijos (nombre y color) directamente en la llamada interna a `super()`. |
| Getters y Setters puros (`getLados()`) | Atributo protegido (`_lados`) y `@property` | Rediseño | Python descarta el boilerplate de getters/setters inútiles. Se usó el encapsulamiento por convención y una `@property` para devolver una `tuple` inmutable como copia defensiva. |
| Parámetro `List lados = new ArrayList()` | `lados=None` en la firma, luego `[]` | Traducción idiomática | Traducir literalmente a `lados=[]` en la firma genera el bug del "default mutable" en Python, compartiendo el mismo espacio de memoria entre todas las instancias. |


## Cierre: ¿Qué cambió y qué se mantuvo idéntico?

Al migrar de Java a Python, **lo que se mantuvo idéntico fue el diseño del dominio y sus relaciones estructurales abstractas**. El modelo de negocio no cambió: un Triángulo sigue siendo un Polígono (herencia estricta), el Taller sigue agrupando figuras que vienen desde el exterior (agregación donde la parte sobrevive al todo), y los Polígonos siguen construyendo sus propios lados internamente (composición estricta de ciclo de vida). 

Por el contrario, **lo que cambió profundamente fue la arquitectura para lograr polimorfismo, dictada por la sintaxis y el sistema de tipado de cada lenguaje**. En Java, estábamos forzados a que `PoligonoRegular` a herede de `Poligono` simplemente porque el compilador necesitaba un "tipo estático compartido" para meterlos en una lista. En Python, esa burocracia desaparece. El rediseño hacia Python nos permitió limpiar el modelo usando Duck Typing y Protocolos estructurales: ahora el código agrupa objetos porque "saben hacer lo mismo" (como exportarse o calcular su perímetro). El diseño de dominio mandó, y la flexibilidad de la sintaxis de Python se adaptó a él.