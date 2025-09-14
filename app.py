import streamlit as st
import time
from src.helper import *
import asyncio


    


import streamlit as st
import time
# Assuming helper functions get_pdf_text, get_text_chunks, get_vector_store, and get_conversational_chain are in a separate file or defined elsewhere.
# from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

def main():
    st.set_page_config(page_title="Generative AI Project", page_icon=":robot_face:") 
    st.title("Generative AI ")
    st.text("This is an Information Retrieval System using Generative AI.")
    st.header("Developed by Aziz")

    # Initialize session state variables if they don't exist
    if 'conversation_chain' not in st.session_state:
        st.session_state.conversation_chain = None 
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # Get user input
    user_query = st.text_input("Ask your question here:")

    # Process user query if conversation chain and history are set
    if user_query and st.session_state.conversation_chain:
        with st.spinner("Generating response..."):
            response = st.session_state.conversation_chain({
                "question": user_query,
                "chat_history": st.session_state.chat_history
            })
            st.session_state.chat_history = response.get("chat_history")
            time.sleep(1)
            st.success("Response generated!")
            st.write(response.get("answer"))
    elif user_query and not st.session_state.conversation_chain:
        st.warning("Please upload files first before asking a question.")

    with st.sidebar:
        uploaded_files = st.file_uploader(
            "Upload data", accept_multiple_files=True, type="pdf")
        if st.button("Click to upload files"):
            if uploaded_files:
                with st.spinner("Uploading Files"):
                    pdf_docs = get_pdf_text(uploaded_files)
                    text_chunks = get_text_chunks(pdf_docs)
                    vector_store = get_vector_store(text_chunks)
                    st.session_state.conversation_chain = get_conversational_chain(vector_store)
                    st.success("Files uploaded successfully")
            else:
                st.error("Please upload at least one PDF file.")

if __name__ == "__main__":
    main()