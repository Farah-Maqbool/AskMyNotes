import streamlit as st
from backend import query_llm, extract_text_from_pdf, extract_text_from_voice, text_to_voice
from io import BytesIO

st.title("AskMyNotes")
st.write("Upload your PDF or ask your question by voice or text.")
pdf_file = st.file_uploader("Upload file",type="pdf")

if pdf_file is not None:
    result = extract_text_from_pdf(pdf_file)

    if "doc_text" not in st.session_state:
        st.session_state["doc_text"] = result

    prompt = st.chat_input("Write your question here")
    

    if prompt:

        answer = query_llm(st.session_state["doc_text"], prompt)

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            st.write(answer)
    
    voice = st.audio_input("Record Your Question here")

    if voice:
        audio_file = BytesIO(voice.read())
        extract_text_voice = extract_text_from_voice(audio_file)
        
        response = query_llm(st.session_state["doc_text"], extract_text_voice)
        st.write(response)
        result = text_to_voice(response, "en")

        st.audio(result, format='audio/mp3')