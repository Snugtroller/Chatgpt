import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # For interacting with LLM models
from langchain_core.prompts import ChatPromptTemplate  # When you want to add a custom prompt
from langchain_core.output_parsers import StrOutputParser  # Tells how to display

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANG_CHAIN_API_KEY = os.getenv("LANG_CHAIN_API_KEY")

# Check if the API keys are loaded properly
if OPENAI_API_KEY is None:
    st.error("OPENAI_API_KEY not found in environment variables.")
if LANG_CHAIN_API_KEY is None:
    st.error("LANG_CHAIN_API_KEY not found in environment variables.")

# Set environment variables for LangChain and OpenAI
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["LANG_CHAIN_API_KEY"] = LANG_CHAIN_API_KEY
os.environ["LANG_CHAIN_TRACING_V2"] = "true"

# Creating chatbot
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("user", "Question:{question}")
    ]
)

st.title("Chatbot Demo")
input_text = st.text_input("Search the topic you want to ask about:")

# OpenAI LLM Call
llm = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

if input_text:
    try:
        response = chain.invoke({"question": input_text})
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
