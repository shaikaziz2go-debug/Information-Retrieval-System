import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 


def get_pdf_text(pdf_docs):
    """Extracts text from a list of PDF documents."""
    text = ""
    # Iterate over each uploaded file object in the list
    for pdf in pdf_docs:
        # Pass the individual file object to PdfReader
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    """Splits a string of text into smaller, manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    """Creates a FAISS vector store from text chunks using Gemini embeddings."""
    
    # Define a helper function to run the async operation
    async def get_embeddings_async():
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
    # Get or create an event loop to run the async function
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Run the async function until it is complete
    embeddings = loop.run_until_complete(get_embeddings_async())
    
    # Now you can proceed with the rest of your synchronous code
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store


def get_conversational_chain(vector_store):
    """Initializes and returns a conversational retrieval chain using the Gemini model."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain