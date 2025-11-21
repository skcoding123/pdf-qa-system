import streamlit as st
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="PDF Question Answerer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF Question Answerer (100% FREE)")
st.write("Upload a PDF and ask questions about it - No API costs!")

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

# Get Astra DB credentials
ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
ASTRA_DB_REGION = os.getenv("ASTRA_DB_REGION")
ASTRA_DB_TOKEN = os.getenv("ASTRA_DB_TOKEN")

# Check if credentials are available
if not all([ASTRA_DB_ID, ASTRA_DB_REGION, ASTRA_DB_TOKEN]):
    st.error("❌ Missing credentials! Please check your .env file.")
    st.info("Make sure you have: ASTRA_DB_ID, ASTRA_DB_REGION, ASTRA_DB_TOKEN")
    st.stop()

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Split text into chunks
def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=200):
    """Split text into smaller chunks for processing"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Create vector store
def create_vector_store(chunks):
    """Create vector store in Astra DB using HuggingFace embeddings"""
    try:
        # Initialize HuggingFace embeddings (runs locally, FREE!)
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            encode_kwargs={'normalize_embeddings': False}
        )
        
        # Create vector store
        vector_store = AstraDBVectorStore(
            embedding=embeddings,
            collection_name="pdf_documents",
            api_endpoint=f"https://{ASTRA_DB_ID}-{ASTRA_DB_REGION}.apps.astra.datastax.com",
            token=ASTRA_DB_TOKEN,
        )
        
        # Add documents to vector store
        vector_store.add_texts(chunks)
        return vector_store
    except Exception as e:
        raise Exception(f"Error creating vector store: {str(e)}")

# PDF Upload Section
st.header("📤 Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

if uploaded_file is not None:
    if st.button("🔄 Process PDF", key="process_btn"):
        with st.spinner("Processing PDF... This may take a moment"):
            try:
                # Step 1: Extract text
                st.info("📖 Extracting text from PDF...")
                text = extract_text_from_pdf(uploaded_file)
                st.success(f"✅ Extracted text ({len(text)} characters)")
                
                # Step 2: Split into chunks
                st.info("📚 Splitting text into chunks...")
                chunks = split_text_into_chunks(text)
                st.success(f"✅ Created {len(chunks)} chunks")
                
                # Step 3: Create vector store
                st.info("🔄 Creating embeddings and uploading to Astra DB...")
                vector_store = create_vector_store(chunks)
                st.session_state.vector_store = vector_store
                st.session_state.pdf_loaded = True
                st.success("✅ PDF processed successfully! You can now ask questions.")
                
            except Exception as e:
                st.error(f"❌ Error processing PDF: {str(e)}")
                st.info("Troubleshooting tips:")
                st.write("- Make sure your Astra DB token is correct")
                st.write("- Check your internet connection")
                st.write("- Verify the PDF file is not corrupted")

# Question Answering Section
if st.session_state.pdf_loaded:
    st.header("❓ Ask Questions")
    
    # Check if Ollama is running
    with st.expander("⚙️ Ollama Status"):
        try:
            llm = Ollama(model="mistral", base_url="http://localhost:11434")
            test_response = llm.invoke("say hello")
            st.success("✅ Ollama is running correctly!")
        except Exception as e:
            st.warning("⚠️ Ollama might not be running. Make sure to:")
            st.write("1. Open Ollama desktop app")
            st.write("2. Make sure it's running in background")
            st.error(f"Error details: {str(e)}")
    
    question = st.text_input("Enter your question about the PDF:")
    
    if question:
        with st.spinner("🤔 Searching and generating answer..."):
            try:
                # Initialize the local LLM (Ollama)
                llm = Ollama(
                    model="mistral",
                    base_url="http://localhost:11434",
                    temperature=0.7
                )
                
                # Create a retriever from vector store
                retriever = st.session_state.vector_store.as_retriever(
                    search_kwargs={"k": 5}
                )
                
                # Define the prompt template
                prompt_template = ChatPromptTemplate.from_template(
                    """You are a helpful assistant. Answer the question based on the provided context.
                    
Context from PDF:
{context}

Question: {question}

Answer: """
                )
                
                # Create the chain
                chain = (
                    {"context": retriever, "question": RunnablePassthrough()}
                    | prompt_template
                    | llm
                )
                
                # Get the answer
                response = chain.invoke(question)
                
                # Display results
                st.subheader("📖 Answer")
                st.write(response)
                
                # Display source chunks
                st.subheader("📚 Source Chunks Used")
                relevant_docs = retriever.get_relevant_documents(question)
                
                for i, doc in enumerate(relevant_docs, 1):
                    with st.expander(f"Chunk {i} - Relevance"):
                        st.write(doc.page_content)
                
            except Exception as e:
                st.error(f"❌ Error generating answer: {str(e)}")
                if "Connection" in str(e):
                    st.warning("Make sure Ollama is running!")
                    st.info("Open Ollama desktop app and make sure it's in background")

else:
    st.info("👆 Please upload and process a PDF first to ask questions.")
    
    with st.expander("📋 Quick Start Guide"):
        st.write("""
        1. **Prepare**: Make sure Ollama app is running
        2. **Upload**: Click 'Browse files' and select a PDF
        3. **Process**: Click '🔄 Process PDF' button
        4. **Wait**: System will extract text, create chunks, and upload to Astra DB
        5. **Ask**: Type your question in the text box
        6. **Get Answer**: AI will search the PDF and provide answer
        """)
