# pip install langchain langchain-community langchain-groq beautifulsoup4 gradio
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, PyPDFLoader
import gradio as gr

