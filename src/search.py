import os
from dotenv import load_dotenv

from langchain_postgres import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    load_dotenv()

    for key in (
        "DATABASE_URL",
        "PG_VECTOR_COLLECTION_NAME",        
        "GOOGLE_LLM_MODEL",
    ):
        if key not in os.environ:
            raise RuntimeError(f"{key} não está definido em variáveis de ambiente")

    if not question:
      return None        

    # embeddings = GoogleGenerativeAIEmbeddings(
    #    model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001")
    # )

    embeddings = HuggingFaceEmbeddings(
        model_name=os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
        model_kwargs={'device': 'cpu'}
    )

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    docs = store.similarity_search_with_score(question, k=10)
    if not docs:
        return "Não tenho informações necessárias para responder sua pergunta."    
    
    context = "\n\n".join([doc.page_content for doc, score in docs]) 

    prompt = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE
    ).format(contexto=context, pergunta=question)

    llm = ChatGoogleGenerativeAI(      
      model=os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite")
    )    

    try:
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        print(f"Erro ao chamar LLM: {e}")
        return "Não tenho informações necessárias para responder sua pergunta."