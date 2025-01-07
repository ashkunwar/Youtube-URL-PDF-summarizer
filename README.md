# LangChain: Summarize Text From YouTube, Website, or PDF


![WhatsApp Image 2024-12-28 at 17 09 59_40c1935f](https://github.com/user-attachments/assets/8804381b-891f-4702-a463-f3dcfbe3bfdb)


This project leverages LangChain, Groq API, and other libraries to provide an intuitive interface for summarizing text content from YouTube videos, websites, or PDF files.

## Features
- **YouTube Transcript Summarization**: Extracts and summarizes the transcript of a YouTube video.
- **Website Content Summarization**: Fetches and summarizes text content from a given URL.
- **PDF Summarization**: Summarizes the content of uploaded PDF documents.

## How It Works
1. **Input Options**:
   - Provide a YouTube video URL.
   - Enter a generic website URL.
   - Upload a PDF file.

2. **Processing**:
   - For YouTube videos, it extracts the transcript using the `YouTubeTranscriptApi`.
   - For websites, it fetches text content using `UnstructuredURLLoader`.
   - For PDFs, it processes the uploaded file using `PyPDFLoader`.

3. **Summarization**:
   - A pre-defined prompt is used to generate a concise summary of the content using the `ChatGroq` LLM.

4. **Output**:
   - The summarized text is displayed on the Streamlit app interface.

## Technologies Used
- **Streamlit**: For building the web interface.
- **LangChain**: For chaining and managing prompts.
- **ChatGroq**: A powerful LLM API for generating summaries.
- **YouTubeTranscriptApi**: For fetching YouTube video transcripts.
- **PyPDFLoader**: For reading and processing PDF files.
- **UnstructuredURLLoader**: For extracting content from websites.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open the app in your browser and provide your Groq API key in the sidebar.

3. Input a URL (YouTube/website) or upload a PDF file and click "Summarize the Content from YT, Website, or PDF."

## Deployed App
Check out the live application: [LangChain Summarizer App](https://youtube-url-pdf-summarizer-bny.streamlit.app/)

## Project Files
- `app.py`: Main application file.
- `requirements.txt`: List of required Python packages.

## Limitations
- Only works with YouTube videos that have transcripts enabled.
- Summarization quality depends on the provided content and LLM capabilities.
- Requires a valid Groq API key to function.

## License
This project is licensed under the MIT License.

