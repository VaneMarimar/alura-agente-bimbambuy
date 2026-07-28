import os
import time
import streamlit as st
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

st.set_page_config(page_title="Alura Agente - BimBam Buy", page_icon="🤖")

st.title("🤖 Alura Agente — BimBam Buy")
st.write(
    "Agente de IA que responde preguntas sobre las políticas de "
    "reembolsos, envíos, afiliados, garantía y métodos de pago de BimBam Buy."
)

# La API Key se configura como "Secret" en Streamlit Cloud, con el nombre APIKEY
API_KEY = st.secrets.get("APIKEY") or os.environ.get("APIKEY")
os.environ["GOOGLE_API_KEY"] = API_KEY or ""


@st.cache_resource(show_spinner="Cargando documentos y preparando el agente...")
def cargar_agente():
    loader = PyPDFDirectoryLoader("documentos")
    documentos = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documentos)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # Procesamos en lotes pequeños para no superar el límite gratuito de la API
    vectorstore = None
    tamano_lote = 15
    for i in range(0, len(chunks), tamano_lote):
        lote = chunks[i:i + tamano_lote]
        intentos = 0
        while intentos < 5:
            try:
                if vectorstore is None:
                    vectorstore = FAISS.from_documents(lote, embeddings)
                else:
                    vectorstore.add_documents(lote)
                break
            except Exception:
                intentos += 1
                time.sleep(20)
        time.sleep(2)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

    return retriever, llm


def preguntar(pregunta, retriever, llm):
    documentos_relevantes = retriever.invoke(pregunta)
    contexto = "\n\n".join([doc.page_content for doc in documentos_relevantes])

    prompt = (
        "Eres el asistente virtual de BimBam Buy. Responde la pregunta del "
        "usuario utilizando UNICAMENTE la informacion del siguiente contexto "
        "extraido de los documentos oficiales de la empresa. Si la respuesta "
        "no esta en el contexto, di claramente que no tenes esa informacion.\n\n"
        f"Contexto:\n{contexto}\n\n"
        f"Pregunta: {pregunta}\n\n"
        "Respuesta clara y concisa:"
    )

    respuesta = llm.invoke(prompt)
    return respuesta.content, documentos_relevantes


if not API_KEY:
    st.error(
        "No se encontró la API Key. Configurala en "
        "Settings → Secrets con el nombre APIKEY."
    )
    st.stop()

retriever, llm = cargar_agente()

pregunta = st.text_input("Escribí tu pregunta sobre BimBam Buy:")

if pregunta:
    with st.spinner("Buscando la respuesta..."):
        respuesta, fuentes = preguntar(pregunta, retriever, llm)
    st.markdown("### 🤖 Respuesta")
    st.write(respuesta)

    with st.expander("📚 Ver fuentes utilizadas"):
        for doc in fuentes:
            origen = doc.metadata.get("source", "desconocido")
            pagina = doc.metadata.get("page", "?")
            st.write(f"- {origen} (página {pagina})")

st.markdown("---")
st.caption("Ejemplos: ¿Cuál es la política de reembolsos? / ¿Cómo funciona el programa de afiliados? / ¿Cuánto tarda el envío?")
