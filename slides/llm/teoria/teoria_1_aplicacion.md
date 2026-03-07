# Tema 1: Introducción a los SR

## ¿Por qué surgen los SR?

- **Cambio del modelo de consumo:** Economía long-tail.
- **Sobrecarga de información:** Infoxicación.

### Economía Long-Tail

- Anderson ("The Long Tail", 2004): economía long-tail — transformación de la venta en espacio físico limitado a venta ilimitada online.
- Espacio físico limitado → pocos productos → satisfacen gustos típicos.
- Espacio físico ilimitado → muchos productos → satisfacen gustos diversos.
- **Cabeza corta (Head):** pocos productos con gran volumen de ventas.
- **Larga cola (Long Tail):** muchos productos con bajo volumen de ventas.


### Auge de los SR

- Los usuarios tienen limitaciones biológicas, temporales y materiales ante la gran cantidad de información disponible.
- Deben elegir qué película ver, qué canción escuchar, qué producto comprar o qué noticia leer.
- Anderson (2007): los algoritmos generan predicciones automáticas acerca de los intereses de un usuario, ayudando en la selección. Pasamos de una era de la información a una era de la recomendación.
- El primer SR fue **Tapestry** (Goldberg, 1992): correo electrónico experimental con filtrado colaborativo.

## Problema: Infoxicación

- Excesivo volumen de información que no se adapta a las necesidades del usuario, proveniente de fuentes heterogéneas sin combinar.
- La búsqueda con IA alivia el problema pero puede no ser fiable.

### Motores de búsqueda

- **Ventajas:** Eliminan gran cantidad de información no deseada.
- **Inconvenientes:** No se adaptan al usuario, producen excesivo volumen de resultados, priorizan según intereses económicos; el usuario refina la búsqueda.

### IA en búsquedas

- Entiende la intención del usuario, ofreciendo respuestas directas en lugar de listas de enlaces.
- Personaliza los resultados y mejora velocidad/calidad con ML y NLP.
- **Ejemplos:** Google Gemini, Microsoft Bing/Copilot, Perplexity AI, GPT (Search Generative Experience).
- **Problemas:**
  - **Alucinaciones:** Información inexacta por predicción de patrones; la IA puede inventarse hechos.
  - **Tiempo real:** Desfase entre nueva información y el conocimiento de la IA (meses o años).
  - **Otros:** Sesgos de entrenamiento, falta de privacidad, anuncios publicitarios.
- **Conclusión:** Para temas importantes (científicos, médicos), los motores de búsqueda con múltiples fuentes son más seguros.

## Sistemas adaptables vs. adaptativos

- **Adaptables:** El usuario busca e interacciona; refina la búsqueda si es necesario. Ej.: motores de búsqueda, IA.
- **Adaptativos:** El sistema decide lo que el usuario necesita y se lo ofrece automáticamente. Ej.: sistemas recomendadores.

## Sistema Recomendador (SR)

- Tipo específico de filtro de información adaptativo.
- Presenta al usuario solo información de su interés, adelantándose a sus necesidades.
- Recomendar = hacer una predicción sobre los intereses del usuario.

## Historia de los SR

### Década 1990

- **Tapestry** (Goldberg, 1992): Correo experimental con filtrado colaborativo.
- **GroupLens** (Resnick, 1994): Noticias.
- **MovieLens** (Konstan, 1997): Primer SR con ratios; recomendador de películas con dataset aún utilizado.
- **Firefly** (Maes, 1997): SR de música; calificación y etiquetado para construir perfiles.

### Década 2000

- Internet se populariza; los SR cobran importancia.
- **Amazon (1994):** Datos de compra y navegación para identificar patrones y generar recomendaciones.
- **Netflix (1998):** Desarrolló Cinematch con ML y filtrado colaborativo sobre historial de visualizaciones.

### Década 2010

- Algoritmos avanzados: descomposición matricial y redes neuronales.
- Recomendación contextual y social: ubicación, dispositivo, momento del día, conexiones sociales.

### Década 2020

- Deep Learning y NLP para mayor personalización.
- Énfasis en privacidad, ética y nuevos dominios (salud, educación, turismo).

## Usos de los SR

| Industria | Aplicaciones |
|---|---|
| **Streaming** | Netflix, Amazon Prime, Spotify, YouTube: sugerencias según preferencias e historial. |
| **Comercio electrónico** | Amazon, eBay, Alibaba: productos personalizados. |
| **Redes sociales** | TikTok, Facebook, Instagram, X: amistades, publicaciones, anuncios. |
| **Noticias** | Google News: contenido según intereses y comportamiento de lectura. |
| **Viajes y reservas** | Booking, Airbnb, TripAdvisor: destinos según historial. |
| **Comida a domicilio** | Uber Eats, Grubhub, Deliveroo: restaurantes y cocinas sugeridas. |
| **Educación online** | Coursera, Udemy, Khan Academy: cursos según intereses y habilidades. |
| **Motores de búsqueda** | Google, Bing: resultados relevantes. |

**Objetivo:** Fidelizar clientes, aumentar ventas/consumo y retener atención.

## Casos específicos

### TikTok

- Feed "Para ti" basado en: intereses expresados, interacciones (compartidos, comentarios, cuentas seguidas), información del vídeo (subtítulos, sonidos, hashtags) y configuración del dispositivo (menor peso).
- No muestra dos vídeos seguidos del mismo creador/sonido; evita duplicados y spam.
- Prioriza vídeos más lucrativos (ratio de publicación, retención).

### YouTube

- Objetivo: retener al usuario el mayor tiempo posible.
- Evalúa en tiempo real cientos de horas subidas por segundo.
- Usa redes neuronales y SR colaborativo para asignar un ranking (puntuación a cada vídeo).

### Netflix

- El 75% de los contenidos consumidos son recomendados.
- Basado en: gustos del usuario (SR contenido), relación con contactos (SR colaborativo) y similitudes de catálogo.
- Factores: interacciones, información de títulos, hora del día, dispositivo, tiempo consumido.
- No incluye información demográfica (edad o género).
- Títulos recientes tienen más peso; sin historial, se usa recomendación mayoritaria.

### Spotify

- Objetivo: evitar que el usuario se canse de escuchar siempre lo mismo.
- 3 tipos de recomendadores: SR colaborativo, modelo de audio en bruto (CNN), NLP + big data.

### Amazon

- Recomendaciones basadas en: elementos similares a los buscados y elementos comprados junto con el buscado.

## Campos de aplicación y Futuro

**Campos de aplicación:** Medicina, agricultura, conducción, enseñanza, ocio, publicidad personalizada.

### Ventajas e inconvenientes

- **Usuarios:**
  - *Ventajas:* Filtra información irrelevante; provee necesidades sin preguntar; ofrece novedades.
  - *Inconvenientes:* Recomendación guiada por intereses económicos; falta de privacidad al compartir preferencias.
- **Servicios y aplicaciones:**
  - *Ventajas:* Interacción efectiva; fidelización; aumenta ventas/retención; mejora con el uso.
  - *Inconvenientes:* Usuarios puntúan favorablemente para perjudicar a la competencia.

### Presente y Futuro

- **IA:** Redes neuronales, ML, Deep Learning, NLP.
- **Visión por computador:** Moda, joyería.
- **Time-aware RS:** Dimensión temporal; preferencias que cambian con el tiempo.
- **Privacidad:** Perfiles encriptados (clave en salud o finanzas).
- **Explicación de resultados:** Incrementa satisfacción, evita opacidad.
- **Contextualización:** Ubicación, tiempo atmosférico, estado de ánimo.
- **SR Conversacionales:** Interacción para refinar la recomendación.
- **Diversidad:** Recomendar ítems diversos en lugar de muy similares.
- **Autoevaluación:** Feedback indirecto para ajustar el SR en tiempo real.

## Consideraciones éticas

Los SR no son ni buenos ni malos; el uso que les dan los servicios determina si son perjudiciales o beneficiosos.

- **Positivos:** Comodidad, ahorro de tiempo, gran utilidad en la personalización.
- **Negativos:**
  - **Información de usuarios:** Recopilación de datos muchas veces sin que el usuario conozca los términos.
  - **Algoritmos opacos:** No se sabe en qué se basan ni cómo toman decisiones; dificulta detectar manipulación.
  - **Burbuja de filtros:** Refuerza ideas del usuario, aumentando extremismo y polarización.
  - **(In)Justicia algorítmica:** Los algoritmos pueden perpetuar y amplificar prejuicios presentes en los datos.
  - **Manipulación:** Por usuarios (feedback falso) o empresas (cuentas falsas para promover productos).
