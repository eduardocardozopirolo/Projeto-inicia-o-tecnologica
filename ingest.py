from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore


PASTA_DOCUMENTOS = "documentos"

# ========================================
# 1. CARREGAR PDFs
# ========================================

documentos = []

for arquivo in Path(PASTA_DOCUMENTOS).glob("*.pdf"):

    print(f"Carregando: {arquivo}")

    loader = PyPDFLoader(str(arquivo))

    docs = loader.load()

    documentos.extend(docs)


print(f"Total de páginas carregadas: {len(documentos)}")


# ========================================
# 2. DIVIDIR EM CHUNKS
# ========================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documentos)

print(f"Total de chunks: {len(chunks)}")


# ========================================
# 3. MODELO DE EMBEDDINGS
# ========================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# ========================================
# 4. SALVAR NO QDRANT
# ========================================

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="artigos_cientificos"
)


print("Documentos indexados no Qdrant!")