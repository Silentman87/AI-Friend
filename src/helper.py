from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

# Extract data from the pdf files
def load_pdf_file(data): 
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    
    documents = loader.load()
    
    return documents


# Split the data into chunks 
def text_split(extracted_data) : 
    text_spliter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap = 20)
    text_chunks = text_spliter.split_documents(extracted_data)
    return text_chunks


# Download the vector embedding model from huggingface
def download_hugging_face_embeddings() : 
    emebeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
    return emebeddings