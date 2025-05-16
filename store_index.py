#############################################################################
#                      AI-Friend | Ai-powered health &                      #
#                          emotional support chatbot                        #
#                                                                           #             
#                                                                           #
#############################################################################


#############################################################################
#  Importing library
#
#############################################################################


from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os



#############################################################################
#  setting the environment variables
#
#############################################################################

load_dotenv()

PINECONE_API_KEY = os.environ.get('PineConeAPi')
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY


#############################################################################
#  Load the pdf 
#  Split it into chunks
#  Download the embedding model
#############################################################################

extracted_data = load_pdf_file(data = 'dataset/')
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()



#############################################################################
#  Creating Pinecone index for storing chunks in vector form
#
#############################################################################

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "aifriend"

pc.create_index(
    name = index_name,
    dimension=384,
    metric="cosine",
    spec = ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

#############################################################################
# Embed each chunk and upsert the embeddings into your pinecone index.
#
#############################################################################

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name = index_name,
    embedding=embeddings,
)



