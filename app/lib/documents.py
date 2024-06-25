import pinecone
import requests
from decouple import config
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone

pinecone.init(
    api_key=config("PINECONE_API_KEY"),
    environment=config("PINECONE_ENVIRONMENT")
)

async def upsert_document(url: str, type: str, document_id: str) -> None:
    pinecone.Index("arrodes")

    embeddings = OpenAIEmbeddings()

    if type == "TXT":
        file_response = requests.get(url)
        loader = TextLoader(file_response.content)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        
        Pinecone.from_documents(
            docs, embeddings, index_name="arrodes", namespace=document_id
        )

    if type == "TXT":
        file_response = requests.get(url)
        loader = PyPDFLoader(file_path=url)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        
        Pinecone.from_documents(
            docs, embeddings, index_name="arrodes", namespace=document_id
        )