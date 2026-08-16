# RAG local para artigos científicos

Este projeto implementa um fluxo simples de **Retrieval-Augmented Generation (RAG)** para fazer perguntas sobre documentos PDF. Os arquivos são processados com LangChain, transformados em embeddings pelo Ollama e armazenados no Qdrant. Durante a consulta, o trecho mais relevante é recuperado e enviado como contexto para um modelo de linguagem local.

## Como funciona

1. O `ingest.py` carrega os PDFs da pasta `documentos/`.
2. Cada documento é dividido em chunks de 1.000 caracteres, com sobreposição de 200 caracteres.
3. O modelo `nomic-embed-text`, executado pelo Ollama, gera os embeddings.
4. Os vetores são armazenados na coleção `artigos_cientificos` do Qdrant.
5. O `chat.py` recupera o chunk mais semelhante à pergunta.
6. O modelo `llama3.2:1b` responde usando o contexto recuperado.

## Tecnologias

- Python
- LangChain
- Ollama
- Qdrant
- PyPDF

## Pré-requisitos

Antes de executar o projeto, instale:

- Python 3.10 ou superior
- [Ollama](https://ollama.com/)
- [Docker](https://www.docker.com/) para executar o Qdrant

Baixe os modelos utilizados pelo projeto:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2:1b
```

Certifique-se também de que o Ollama está em execução. Quando necessário, inicie-o com:

```bash
ollama serve
```

## Instalação

Clone ou acesse a pasta do projeto e crie um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows PowerShell, ative o ambiente com:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências Python:

```bash
pip install langchain-community langchain-text-splitters langchain-ollama langchain-qdrant pypdf
```

## Executando o Qdrant

Inicie uma instância local do Qdrant na porta `6333`:

```bash
docker run --name qdrant-rag \
  -p 6333:6333 \
  -p 6334:6334 \
  -v "$(pwd)/qdrant_storage:/qdrant/storage" \
  qdrant/qdrant
```

Nas próximas execuções, se o contêiner já existir, use:

```bash
docker start qdrant-rag
```

## Adicionando documentos

Coloque os arquivos PDF que deseja consultar na pasta:

```text
documentos/
```

Em seguida, execute a indexação:

```bash
python ingest.py
```

O script criará ou preencherá a coleção `artigos_cientificos` no Qdrant.

> **Atenção:** executar a ingestão repetidamente sobre os mesmos PDFs pode inserir chunks duplicados na coleção. Para uma nova base, remova ou recrie a coleção antes de reindexar.

## Fazendo uma pergunta

Com o Ollama e o Qdrant em execução e os documentos já indexados, execute:

```bash
python chat.py
```

Digite a pergunta quando solicitado:

```text
Pergunta: O que é o mecanismo de atenção?
```

O sistema buscará o trecho mais próximo semanticamente e solicitará ao modelo uma resposta baseada somente nesse contexto.

## Estrutura do projeto

```text
.
├── chat.py             # Recupera contexto e gera a resposta
├── ingest.py           # Carrega, divide e indexa os PDFs
├── documentos/         # PDFs usados como fonte de conhecimento
├── qdrant_storage/     # Persistência local do banco vetorial
└── README.md
```

## Configurações principais

As configurações atuais estão definidas diretamente nos scripts:

| Configuração | Valor |
| --- | --- |
| URL do Qdrant | `http://localhost:6333` |
| Coleção | `artigos_cientificos` |
| Modelo de embeddings | `nomic-embed-text` |
| Modelo de linguagem | `llama3.2:1b` |
| Chunks recuperados por pergunta | `1` |
| Temperatura | `0` |

Para alterar esses valores, edite `ingest.py` e `chat.py`, mantendo o mesmo modelo de embeddings e o mesmo nome de coleção nos dois arquivos.

## Solução de problemas

- **Erro de conexão com o Qdrant:** confirme que o contêiner está ativo e que a porta `6333` está disponível.
- **Modelo não encontrado:** execute novamente os comandos `ollama pull` da seção de pré-requisitos.
- **Coleção inexistente:** execute `python ingest.py` antes de iniciar o chat.
- **Nenhum documento carregado:** confirme que os arquivos têm extensão `.pdf` e estão dentro de `documentos/`.
- **Resposta incompleta:** atualmente apenas um chunk, limitado a 800 caracteres no prompt, é usado como contexto. Ajuste `k` e o recorte de `page_content` em `chat.py` se necessário.

## Limitações atuais

- O chat processa uma pergunta por execução.
- A resposta usa somente um trecho recuperado.
- Não há interface web nem histórico de conversa.
- Os parâmetros e nomes dos modelos não são configuráveis por variáveis de ambiente.
