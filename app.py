import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_groq import ChatGroq
from langchain.schema import Document
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.document_loaders import PyPDFLoader
import validators
import re
import os

# Streamlit App Configuration
st.set_page_config(page_title="LangChain: Summarize Text From YT, Website, or PDF", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT, Website, or PDF")
st.subheader("Summarize URL or PDF")

# Sidebar for API Key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="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", type="password")

# Input URL or File
generic_url = st.text_input("URL", label_visibility="collapsed")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# LLM Configuration
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

# Summarization Prompt Template
prompt_template = """
Provide a summary of the following content in 300 words:
Content: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# Function to Extract Video ID
def get_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Button to Summarize Content
if st.button("Summarize the Content from YT, Website, or PDF"):
    if not groq_api_key.strip() or (not generic_url.strip() and not uploaded_file):
        st.error("Please provide a URL or upload a PDF file.")
    elif generic_url and not validators.url(generic_url):
        st.error("Please enter a valid URL. It can be a YouTube video URL or a website URL.")
    else:
        try:
            with st.spinner("Fetching content..."):
                if uploaded_file:
                    # PDF Summarization
                    temp_file_path = f"temp_{uploaded_file.name}"
                    with open(temp_file_path, "wb") as temp_file:
                        temp_file.write(uploaded_file.read())

                    loader = PyPDFLoader(file_path=temp_file_path)
                    docs = loader.load()

                    # Chain for Summarization
                    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                    output_summary = chain({"input_documents": docs})

                    # Display the summarized text
                    st.success(output_summary["output_text"])

                    # Clean up the temporary file
                    os.remove(temp_file_path)

                elif "youtube.com" in generic_url or "youtu.be" in generic_url:
                    # YouTube Transcript Summarization
                    video_id = get_video_id(generic_url)
                    if not video_id:
                        st.error("Invalid YouTube URL. Please check and try again.")
                    else:
                        # Fetch transcript
                        transcript = YouTubeTranscriptApi.get_transcript(video_id)
                        transcript_text = " ".join([entry["text"] for entry in transcript])

                        # Convert transcript to list of documents
                        docs = [Document(page_content=transcript_text)]

                        # Chain for Summarization
                        chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                        output_summary = chain({"input_documents": docs})

                        # Display the summarized text
                        st.success(output_summary["output_text"])

                else:
                    # Generic URL Summarization
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                    )
                    docs = loader.load()

                    # Chain for Summarization
                    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                    output_summary = chain({"input_documents": docs})

                    # Display the summarized text
                    st.success(output_summary["output_text"])

        except TranscriptsDisabled:
            st.error("Transcripts are disabled for this video.")
        except VideoUnavailable:
            st.error("The video is unavailable. Please check the URL.")
        except Exception as e:
            st.exception(f"Exception: {e}")
