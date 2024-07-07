import pinecone
from decouple import config
from langchain.vectorstores.pinecone import Pinecone

pinecone.init(
    api_key=config("PINECONE_API_KEY"), 
    environment=config("PINECONE_ENVIRONMENT"), 
)

pinecone.Index("superagent")


class PineconeVectorstore:
    def __init__(self):
        pass
    
    def from_documents(self, docs, embeddings, index_name, namespace):
        Pinecone.from_documents(
            docs, embeddings, index_name="arrodes", namespace=namespace
        )
    def from_existing(self, embeddings, namespace):
        Pinecone.from_existing_index(
            "arrodes", embeddings, namespace=namespace
        )
