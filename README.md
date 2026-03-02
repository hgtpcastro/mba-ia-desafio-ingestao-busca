# Desafio MBA Engenharia de Software com IA - Full Cycle

Pipeline RAG (Retrieval-Augmented Generation) que ingere PDFs, gera embeddings e permite consultar documentos através de uma interface CLI.

## 🎯 Objetivo

Demonstrar um fluxo completo de:
1. Ingestão de documentos PDF
2. Geração de embeddings com modelos HuggingFace
3. Armazenamento em PostgreSQL com pgvector
4. Busca semântica e geração de respostas com IA

## 📁 Estrutura

| Arquivo | Descrição |
|---------|-----------|
| `src/ingest.py` | Carrega PDF, divide em chunks (1000 caracteres com overlap 150) e gera embeddings |
| `src/search.py` | Configura cadeia RAG: busca vetorial + LLM para responder perguntas |
| `src/chat.py` | Interface CLI interativa para fazer perguntas sobre o documento |
| `docker-compose.yml` | PostgreSQL 17 com pgvector pré-configurado |

## 🚀 Quick Start

### 1. Inicie o banco de dados
```bash
docker compose up -d
```

### 2. Configure o ambiente
```bash
# Crie um arquivo .env na raiz do projeto
cat > .env << EOF_ENV
# Google Gemini configuration
GOOGLE_API_KEY=
GOOGLE_LLM_MODEL=gemini-2.5-flash-lite

# Huggingface configuration
HF_TOKEN=
HF_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Database configuration
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documents

# PDF file path
PDF_PATH=document.pdf
EOF_ENV
```

### 3. Instale dependências
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 4. Configure a API Google
```bash
# Exporte sua chave de API Google
export GOOGLE_API_KEY="sua_chave_aqui"
```

### 5. Ingira o documento
```bash
python src/ingest.py
```
📝 Coloque um arquivo `document.pdf` na raiz do projeto antes de executar.

### 6. Execute o chat
```bash
python src/chat.py
```

Digite suas perguntas e pressione Enter. Para sair, digite `quit`, `exit`, `sair` ou deixe em branco.

## 🔧 Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `PDF_PATH` | Diretório contendo `document.pdf` | `.` ou `/home/user/docs` |
| `DATABASE_URL` | Conexão PostgreSQL | `postgresql://postgres:postgres@localhost:5432/rag` |
| `PG_VECTOR_COLLECTION_NAME` | Nome da coleção de vetores | `document_chunks` |
| `HF_EMBEDDING_MODEL` | Modelo de embedding HuggingFace | `sentence-transformers/all-MiniLM-L6-v2` |
| `GOOGLE_LLM_MODEL` | Modelo LLM do Google | `gemini-2.5-flash-lite` |
| `GOOGLE_API_KEY` | Chave da API Google Generative AI | ⚠️ Obrigatória |

## 📋 Pré-requisitos

- Python 3.10+
- Docker & Docker Compose
- Chave de API do Google Generative AI
- Documento PDF para análise

## 🔍 Como Funciona

```
PDF → Chunks → Embeddings → PostgreSQL+pgvector
                                  ↓
                    Pergunta → Busca Vetorial → Top-10 Documentos
                                  ↓
                          Contexto + Prompt → LLM → Resposta
```

1. **Ingestão**: PDF dividido em chunks de 1000 caracteres com overlap de 150
2. **Embeddings**: Cada chunk convertido em vetor usando HuggingFace
3. **Armazenamento**: Vetores guardados em PostgreSQL com extensão pgvector
4. **Busca**: Perguntas vetorizadas e comparadas com chunks armazenados
5. **Resposta**: Top-10 chunks relevantes formam contexto para LLM gerar resposta

## ⚠️ Observações Importantes

- O banco PostgreSQL é criado automaticamente no primeiro `docker compose up`
- Se não houver `document.pdf`, o script de ingestão encerra silenciosamente
- A LLM responde apenas com informações presentes no documento
- O modelo de embedding é baixado automaticamente na primeira execução

## 🛠️ Troubleshooting

**PostgreSQL não conecta**
```bash
docker compose up -d
docker compose logs postgres
docker compose ps
```

**Erro ao carregar modelo de embedding**
```bash
# Verifique conexão com HuggingFace
python -c "from sentence_transformers import SentenceTransformer; \
           SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

**Erro na API Google (404 model not found)**
- Confirme que `GOOGLE_API_KEY` está definida
- Verifique modelos disponíveis na [Google AI Studio](https://aistudio.google.com/)
- Alguns modelos podem exigir acesso habilitado na Google Cloud Console

**Nenhum documento encontrado**
```bash
ls -la document.pdf  # Confirme que o arquivo existe e está no diretório raiz
python src/ingest.py  # Rode novamente
```

## 📚 Referências

- [LangChain Documentation](https://www.langchain.com/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [HuggingFace Sentence Transformers](https://huggingface.co/sentence-transformers)
- [Google Generative AI API](https://ai.google.dev/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
