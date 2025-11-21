# 📄 PDF Question Answerer - 100% FREE

A powerful open-source web application that lets you upload any PDF and ask questions about its content. Get intelligent answers powered by **local AI models** with **zero API costs**.

## ✨ Features

- 📤 **Easy PDF Upload**: Upload any PDF file
- 🤖 **Local AI Processing**: Uses HuggingFace embeddings (runs locally)
- 🔍 **Intelligent Search**: Finds relevant content in your PDF
- 💬 **Natural Conversations**: Ask unlimited questions about your PDF
- 📚 **Source Attribution**: See which PDF chunks were used for answers
- 💰 **100% FREE**: No API costs, no subscriptions
- 🔐 **Privacy**: All processing can be done locally
- ⚡ **Fast**: Instant answers with source references

## 🎯 How It Works

```
PDF Upload
    ↓
Extract Text
    ↓
Split into Chunks
    ↓
Create Embeddings (HuggingFace - FREE!)
    ↓
Store in Astra DB
    ↓
User Asks Question
    ↓
AI Searches Similar Chunks
    ↓
Returns Answer with Sources
```

## 🛠️ Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| **Embeddings** | HuggingFace (local) | FREE ✅ |
| **LLM** | Ollama (local) | FREE ✅ |
| **Vector DB** | Astra DB | FREE ✅ |
| **Web UI** | Streamlit | FREE ✅ |
| **Framework** | LangChain | FREE ✅ |
| **PDF Processing** | PyPDF | FREE ✅ |

## 📋 Prerequisites

- **Python 3.9+** installed
- **Ollama** desktop app downloaded
- **Astra DB** free account
- **Git** (optional, for cloning)
- **VS Code** or any code editor

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/pdf-question-answerer.git
cd pdf-question-answerer
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Ollama

1. Download Ollama from https://ollama.ai/
2. Install and open the app
3. Download Mistral model:
```bash
ollama pull mistral
```

### 5. Setup Astra DB

1. Create free account at https://astra.datastax.com/
2. Create database named `pdf-qa`
3. Get your credentials:
   - **Database ID** (from connection string)
   - **Region** (from connection string)
   - **Token** (generate in Tokens section)

### 6. Create .env File

Create `.env` file in project root:

```env
ASTRA_DB_ID=your_database_id_here
ASTRA_DB_REGION=your_region_here
ASTRA_DB_TOKEN=your_token_here
```

**Example:**
```env
ASTRA_DB_ID=a1b2c3d4e5f6g7h8
ASTRA_DB_REGION=us-east-1
ASTRA_DB_TOKEN=AstraCS:a1b2c3d4e5f6:xyz789abc123...
```

### 7. Run Application

1. Make sure Ollama desktop app is running
2. Run:
```bash
streamlit run app.py
```
3. Browser opens at `http://localhost:8501`

## 📖 Usage

### Upload PDF

1. Click **"Browse files"** button
2. Select any PDF file
3. Click **"🔄 Process PDF"** button
4. Wait for processing (1-2 minutes for large PDFs)

### Ask Questions

1. Type your question in the text box
2. Examples:
   - "What is this document about?"
   - "Summarize the main points"
   - "What is mentioned about [topic]?"
3. Press Enter or click outside box
4. AI generates answer in 10-30 seconds

### View Sources

- Expand **"Source Chunks Used"** section
- See which parts of PDF were used
- Verify accuracy of answers

## 🔧 Configuration

### Adjust Chunk Size

Edit in `app.py`:
```python
def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=200):
```

- **chunk_size**: Larger = more context, slower processing
- **chunk_overlap**: Larger = better context continuity

### Use Different Embedding Model

In `create_vector_store()`:
```python
embeddings = HuggingFaceEmbeddings(
    model_name="all-mpnet-base-v2"  # Try different models
)
```

Options:
- `all-MiniLM-L6-v2` (Fast, accurate - default)
- `all-mpnet-base-v2` (Slower, more accurate)
- `distiluse-base-multilingual-cased-v2` (Multilingual)

### Use Different LLM Model

Edit:
```python
llm = Ollama(
    model="mistral",  # Change this
    base_url="http://localhost:11434"
)
```

Available models:
```bash
ollama pull llama2
ollama pull neural-chat
ollama pull orca-mini
```

## 📊 Project Structure

```
pdf-question-answerer/
├── app.py                  # Main application
├── requirements.txt        # Python dependencies
├── .env                    # Your credentials (NOT in Git)
├── .gitignore             # Exclude sensitive files
├── README.md              # This file
└── example_pdfs/          # Sample PDFs (optional)
    └── sample.pdf
```

## ⚙️ Troubleshooting

### Error: "No module named 'streamlit'"

```bash
# Make sure venv is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Reinstall packages
pip install -r requirements.txt
```

### Error: "Missing credentials"

1. Check `.env` file exists in project root
2. Check credentials are correct (no extra spaces)
3. Token should start with `AstraCS:`
4. Reload app: Press Ctrl+C and run again

### Error: "Connection refused" (Ollama)

1. Open Ollama desktop app
2. Make sure it's running in taskbar/system tray
3. Restart Ollama if needed
4. Verify model: `ollama list`

### Error: "Cannot extract PDF text"

- PDF might be scanned image (needs OCR)
- PDF might be corrupted
- Try different PDF file

### Slow Processing

**First time:**
- Embedding model downloads (~500MB)
- Takes 2-3 minutes

**Large PDFs:**
- 100+ pages takes longer
- Normal behavior, just wait

### No Answer Generated

1. Check Ollama is running
2. Check internet connection (for Astra DB)
3. Try simpler question
4. Check "Ollama Status" in app

## 🔒 Security & Privacy

- ✅ **Local Processing**: Embeddings & LLM run on your computer
- ✅ **No Data Sent to APIs**: Only to Astra DB for storage
- ✅ **No API Keys Exposed**: Credentials in `.env` (excluded from Git)
- ✅ **Open Source**: Audit the code yourself
- ✅ **No Tracking**: No analytics or telemetry

**Add to `.gitignore`:**
```
.env
.venv/
__pycache__/
*.pyc
.streamlit/
```

## 📈 Performance Tips

1. **Reduce chunk_size** for faster processing (less accurate)
2. **Increase chunk_overlap** for better context
3. **Use smaller embedding model** for faster speed
4. **Use smaller LLM model** for faster answers
5. **Increase RAM** for large PDFs

## 🎓 Learning Resources

### Understanding the Flow

1. **PDF Extraction**: Text extraction from PDF files
2. **Text Chunking**: Breaking long text into manageable pieces
3. **Embeddings**: Converting text to vectors (numbers)
4. **Vector Search**: Finding similar content quickly
5. **RAG Pattern**: Retrieval-Augmented Generation
6. **LLM**: Large Language Models for answer generation

### Key Concepts

- **RAG**: Use retrieved documents to augment LLM responses
- **Embeddings**: Numerical representation of text meaning
- **Vector Database**: Fast similarity search in high dimensions
- **LangChain**: Framework connecting all components
- **Streamlit**: Fast way to build data applications

## 🚀 Future Enhancements

- [ ] Support for multiple PDFs simultaneously
- [ ] Save conversation history
- [ ] Export Q&A to PDF
- [ ] Dark mode UI
- [ ] Advanced filters and search
- [ ] Integration with other document formats (DOCX, PPT)
- [ ] Multi-language support
- [ ] GPU acceleration
- [ ] Web deployment
- [ ] API endpoint

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## ⚠️ Limitations

- Requires internet connection (for Astra DB)
- Ollama requires 8GB+ RAM recommended
- Works best with English documents
- Scanned PDFs (images) not supported without OCR
- Local LLM slower than cloud APIs
- Limited to 2GB+ storage for models

## 💬 Support

- **Issues**: GitHub Issues
- **Questions**: GitHub Discussions
- **Documentation**: See README & comments in code
- **Problems**: Check Troubleshooting section

## 📞 Contact

- **GitHub**: https://github.com/yourusername
- **Email**: your.email@example.com

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Web app framework
- [LangChain](https://www.langchain.com/) - LLM framework
- [HuggingFace](https://huggingface.co/) - Embeddings models
- [Ollama](https://ollama.ai/) - Local LLM runner
- [Astra DB](https://astra.datastax.com/) - Vector database
- [DataStax](https://www.datastax.com/) - Database provider

## 📊 Statistics

- ⭐ Stars: [GitHub Stars]
- 🍴 Forks: [GitHub Forks]
- 👥 Contributors: [Contributors]
- 📥 Downloads: [Downloads]

## 🎉 Ready to Use?

1. Clone this repo
2. Follow Quick Start steps
3. Upload your PDF
4. Ask questions
5. Get answers with sources!

**Enjoy learning with your PDFs! 📚**

---

*Last Updated: 2024 | Version: 1.0 | Status: Active & Maintained*
