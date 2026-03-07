Tienes las tareas a realizar en `slides/llm/tasks.md`.

Las tareas de la sesión 1 son más generales y abarcan todo el proyecto, simplemente tómalas como orientación pero no las hagas todas si van más allá de las otras sesiones. Añade un tag en git cuando hayas terminado cada sesión. NO hagas tareas de más que no se indiquen en la sesión.

No realices ninguna tarea que esté relacionada con la interfaz. O al menos la interfaz en este momento debe de ser muy básica, incluida en el código de Python y desde CLI, sin nada de frontend ni nada visual. Solo texto. La interfaz visual se hará en la última sesión que no tienes que realizar en este momento.

Cada tarea debes de hacer un commit específico para esa tarea, con un mensaje claro y descriptivo. Por ejemplo, si haces la tarea de crear el perfil de usuario, el mensaje del commit podría ser "Crear perfil de usuario con vector de preferencias e histórico de interacción".

Ya se ha realizado un trabajo previo con el dataset en el archivo `src/preprocessing/crearDatasets.py`. Puedes usar ese código como base, pero es posible que debas corregir o adaptar alguna parte porque no estoy seguro de si cumple con las especificaciones que se indican sobre las tareas.

Además de estas especificaciones, en `slides/llm/trabajo/*.md` tienes 4 ficheros markdown sobre las slides de clase que se han dado hasta ahora, con información importante sobre los conceptos, metodología y técnicas que tienes que aplicar en cada tarea. Es MUY IMPORTANTE que leas estos ficheros antes de empezar a hacer las tareas, para entender bien lo que tienes que hacer y cómo hacerlo. No te limites a hacer las tareas sin entender el contexto y la teoría detrás de ellas.

No se trata de resolver las tareas de cualquier forma, sino siguiendo las indicaciones que se han dado en clase sobre las mismas. Cualquier desviación de las indicaciones o cualquier solución que no siga la metodología y técnicas explicadas en clase, no será considerada válida. Por ejemplo, si se indica que el vector de preferencias debe tener 20 géneros y una escala de 0-100, no puedes hacer un vector con 10 géneros o con una escala de 0-5. Si se indica que debes usar la correlación de Pearson para calcular la afinidad entre usuarios, no puedes usar otra métrica como la distancia euclidiana o el coseno de similitud. Al menos de momento en esta fase inicial.

En `slides/llm/teoria/*.md` tienes 4 ficheros markdown sobre las slides de clase que se han dado hasta ahora en las clases de teoría. Estas se centran más en los conceptos teóricos que en las especificaciones para el trabajo y te pueden servir para entender mejor la teoría detrás de las tareas y saber qué es lo que hemos visto hasta ahora.

En resumen, sigue las tareas indicadas para cada sesión, haz commits específicos para cada tarea con mensajes claros y descriptivos, y lee los ficheros de las slides de clase para entender bien lo que tienes que hacer y cómo hacerlo. No te saltes ninguna tarea ni hagas tareas de más que no se indiquen en la sesión. Y no hagas nada relacionado con la interfaz visual por ahora, solo una interfaz básica desde CLI.

IMPORTANTE: Cuando quieras realizar procesos de gather de información lo mejor es que utilices subagentes en paralelo para así optimizar el tiempo de procesamiento.