# 🤖 Alura Agente — BimBam Buy

Agente de inteligencia artificial que responde preguntas en lenguaje natural sobre los documentos internos de **BimBam Buy** (política de reembolsos, programa de afiliados, guía de envíos, garantía de productos y preguntas frecuentes sobre métodos de pago), sin necesidad de abrir ningún archivo manualmente.

Este proyecto fue desarrollado como **Challenge Final** del curso de Alura, aplicando técnicas de **RAG (Retrieval-Augmented Generation)** sobre documentos PDF.

---

## 📌 Descripción del proyecto

BimBam Buy es un e-commerce con varios documentos internos (políticas, FAQs, manuales). Las personas que necesitan esta información suelen perder tiempo buscando dentro de cada PDF. Este agente permite hacerle una pregunta directa y recibir una respuesta clara, basada únicamente en el contenido real de los documentos de la empresa.

---

## 🏗️ Arquitectura de la solución

```
PDFs (BimBam Buy)
      │
      ▼
Lectura y extracción de texto (PyPDFDirectoryLoader)
      │
      ▼
División en fragmentos / chunks (RecursiveCharacterTextSplitter)
      │
      ▼
Generación de embeddings (Google Gemini - models/gemini-embedding-001)
      │
      ▼
Base vectorial FAISS (búsqueda por similitud semántica)
      │
      ▼
Recuperación de los fragmentos más relevantes (retriever)
      │
      ▼
Modelo de lenguaje Gemini (gemini-2.5-flash) + Prompt personalizado
      │
      ▼
Respuesta en lenguaje natural + fuentes citadas
```

El flujo es un patrón clásico de **RAG**: en lugar de que el modelo "invente" una respuesta, primero se buscan los fragmentos de los documentos más relacionados con la pregunta, y luego el modelo de lenguaje redacta la respuesta basándose únicamente en ese contexto.

---

## 🛠️ Tecnologías y herramientas utilizadas

| Herramienta | Uso |
|---|---|
| **Python** | Lenguaje principal del proyecto |
| **Google Colab** | Entorno de desarrollo y prototipado |
| **LangChain** | Orquestación del agente y la cadena RAG |
| **PyPDF** (`PyPDFDirectoryLoader`) | Lectura y extracción de texto de los PDFs |
| **Google Gemini** (`gemini-2.5-flash`) | Modelo de lenguaje que genera las respuestas |
| **Google Gemini Embeddings** (`gemini-embedding-001`) | Generación de vectores semánticos del texto |
| **FAISS** | Base de datos vectorial para búsqueda por similitud |
| **Streamlit** | Interfaz web del agente |
| **Streamlit Cloud** | Plataforma de despliegue en la nube |

---

## 📂 Documentos utilizados

- Política de Reembolsos y Devoluciones de BimBam Buy
- Programa de Afiliados de BimBam Buy
- Guía de Tiempos y Costos de Envío de BimBam Buy
- Manual de Garantía de Productos de BimBam Buy
- Preguntas Frecuentes sobre Métodos de Pago de BimBam Buy

---

## ▶️ Instrucciones para ejecutar el proyecto

### Opción 1: Localmente en Google Colab

1. Abrí el archivo `Alura_Agente_BimBamBuy.ipynb` en [Google Colab](https://colab.research.google.com).
2. Configurá tu API Key de Google Gemini en 🔑 **Secrets** con el nombre `APIKEY` (conseguila gratis en [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)).
3. Ejecutá las celdas **en orden**, de arriba hacia abajo:
   - Instalación de dependencias.
   - Carga de la API Key.
   - Subida de los documentos PDF.
   - Lectura y procesamiento de los documentos.
   - Creación del agente (embeddings + base vectorial + modelo de lenguaje).
   - Función `preguntar()` para hacer consultas.
4. Probá el agente llamando a la función `preguntar("tu pregunta acá")`.

### Opción 2: Desplegado en la nube (Streamlit Cloud)

1. Asegurate de tener en el repositorio: `streamlit_app.py`, `requirements.txt` y la carpeta `documentos/` con los 5 PDFs de BimBam Buy.
2. Andá a [share.streamlit.io](https://share.streamlit.io) e iniciá sesión con tu cuenta de GitHub.
3. Click en **"New app"** → elegí este repositorio → archivo principal: `streamlit_app.py`.
4. En **"Advanced settings" → "Secrets"**, agregá:
   ```
   APIKEY = "tu_clave_de_gemini_aca"
   ```
5. Click en **"Deploy"**. En unos minutos la app queda accesible en una URL pública tipo `https://tu-app.streamlit.app`.

> Nota: el challenge sugiere OCI Compute, pero permite explícitamente usar otras plataformas de deploy (Render, Streamlit Cloud, Railway, etc.). Se optó por Streamlit Cloud por su rapidez y simplicidad para este proyecto.

---

## 💬 Ejemplos de preguntas y respuestas

> Preguntas de prueba realizadas al agente sobre los documentos de BimBam Buy:

**Pregunta:** ¿Cuál es la política de reembolsos de BimBam Buy?
**Respuesta:** _(completar con la respuesta real del agente)_

**Pregunta:** ¿Cómo funciona el programa de afiliados?
**Respuesta:** De acuerdo con el contexto provisto, el programa de afiliados funciona de la siguiente manera: el afiliado recibe un enlace o código rastreable. Cuando se origina una compra válida desde ese canal, la venta puede generar una comisión, siempre que se cumplan las siguientes condiciones: que el pedido sea confirmado, que no exista una anulación fraudulenta, que el pago sea aprobado, y que la compra cumpla con las condiciones de atribución (las cuales dependen de la ventana de conversión, reglas de seguimiento, vigencia del enlace, identificador del afiliado y la validación interna del pedido). Todo este funcionamiento se apoya en el seguimiento técnico, la validación interna y las reglas de conversión previamente definidas por BimBam Buy.
*(Fuentes: Programa de Afiliados de BimBam Buy.pdf, páginas 2, 3, 6, 8)*

**Pregunta:** ¿Cuánto tarda el envío y cuánto cuesta?
**Respuesta:** Basado en los documentos oficiales de BimBam Buy, la información sobre los tiempos y costos de envío es la siguiente:

**Tiempos de envío:** el tiempo total depende de la preparación del pedido y de la zona de entrega. Preparación del pedido: validación de pago (0 a 1 día hábil), alistamiento y empaque (1 a 2 días hábiles), despacho al operador logístico (1 día hábil adicional). Entrega estimada: zonas urbanas principales 2 a 5 días hábiles, zonas secundarias 4 a 8 días hábiles, zonas de cobertura extendida 6 a 12 días hábiles. Los tiempos pueden variar según el país, ciudad, tamaño/peso del producto, clima, campañas especiales o alta demanda.

**Costos de envío:** no hay un costo único. El valor se calcula según el destino, el peso volumétrico y tamaño del paquete, el servicio elegido, promociones vigentes y el umbral de envío gratis (cuando aplique). El costo final se muestra antes de confirmar la compra.
*(Fuentes: Guía de Tiempos y Costos de Envío de BimBam Buy.pdf, páginas 0, 2, 3)*

**Pregunta:** ¿Qué cubre la garantía de los productos?
**Respuesta:** De acuerdo con los documentos oficiales de BimBam Buy, la garantía cubre: falla de encendido, mal funcionamiento de componentes, defectos de ensamblaje, problemas de fabricación, inconsistencias técnicas no originadas por el cliente, y fallas intermitentes, comportamiento anómalo y defectos visibles al primer uso.
*(Fuentes: Manual de Garantía de Productos de BimBam Buy.pdf, páginas 1, 2, 4)*

📸 **Capturas de pantalla del agente respondiendo:**

_(agregar acá las capturas de pantalla del notebook corriendo con las respuestas reales)_

`![Ejemplo de pregunta 1](ruta/a/captura1.png)`

`![Ejemplo de pregunta 2](ruta/a/captura2.png)`

---

## ☁️ Evidencia del deploy en Streamlit Cloud

**URL pública de la aplicación:** _(pegar acá el link `https://tu-app.streamlit.app` una vez desplegada)_

📸 **Captura de la aplicación corriendo:**

_(agregar acá una captura de pantalla mostrando la app funcionando en Streamlit Cloud)_

---

## ✅ Estado del proyecto

- [x] Lectura y procesamiento de documentos (PDF)
- [x] Agente de IA funcional respondiendo preguntas (RAG con Gemini) — **probado y funcionando con 4 preguntas de ejemplo**
- [ ] Deploy en Streamlit Cloud *(completar con el link una vez desplegado)*

---

## 📝 Notas

- El proyecto usa el *tier* gratuito de la API de Google Gemini, que tiene un límite de solicitudes por minuto. El código procesa los documentos en lotes para evitar superar ese límite.
- Este proyecto fue desarrollado como parte del Challenge Final "Alura Agente".
