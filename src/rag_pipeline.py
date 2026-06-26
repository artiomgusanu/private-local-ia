from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

EMBED_MODEL   = 'nomic-embed-text'
LLM_MODEL     = 'phi3:mini'
CHUNK_SIZE    = 500
CHUNK_OVERLAP = 50

def build_vectorstore(text: str, collection: str = 'docs'):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_text(text)
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    return Chroma.from_texts(
        chunks,
        embeddings,
        collection_name=collection,
        persist_directory='./chroma_db'
    )

def build_chain(vectorstore):
    llm = OllamaLLM(model=LLM_MODEL, temperature=0.1)
    retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
    prompt = PromptTemplate(
        input_variables=['context', 'question'],
        template='''És um assistente especializado em analisar documentos.
Responde APENAS com base no contexto abaixo.
Se a informação não estiver no contexto, diz "Não encontrei essa informação no documento."

Responde sempre em português de Portugal.
Usa frases claras e directas.
Se fizer sentido, usa bullet points para organizar a resposta.

Contexto:
{context}

Pergunta: {question}

Resposta:'''
    )
    def format_docs(docs):
        return '\n\n'.join(doc.page_content for doc in docs)

    chain = (
        {'context': retriever | format_docs, 'question': RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain