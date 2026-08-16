from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore

print("1 - Inicializando embeddings...")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

print("2 - Conectando ao Qdrant...")

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="artigos_cientificos",
    url="http://localhost:6333"
)

print("3 - Inicializando LLM...")

llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0
)

print("4 - Tudo carregado!")

pergunta = input("\nPergunta: ")

print("5 - Buscando documentos no Qdrant...")

documentos = vector_store.similarity_search(
    pergunta,
    k=1
)

print("6 - Documentos encontrados!")

contexto = "\n\n".join(
    doc.page_content[:800]
    for doc in documentos
)

print("7 - Enviando contexto para o LLM...")

prompt = f"""
Responda utilizando SOMENTE o contexto abaixo.

CONTEXTO:

{contexto}

PERGUNTA:

{pergunta}
"""

resposta = llm.invoke(prompt)

print("8 - Resposta recebida!")

print(resposta.content)