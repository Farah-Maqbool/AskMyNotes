import google.generativeai as genai
import os
from PyPDF2 import PdfReader
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO


def query_llm(pdf, ques):
    try: 
        api_key = os.getenv("GOOGLE_API_KEY")

        message_send_model = f"""
            You are a teacher for students from class 1 to 5.

            If the user asks a question, answer it using the provided PDF content.

            If the user asks you to generate questions, create a list of questions based on the PDF content.

            PDF Content:
            {pdf}

            User Query:
            {ques}

            Answer:
        """

        genai.configure(api_key=api_key)
        config = {
            "temperature" : 0.5,
            "response_mime_type": "text/plain"
        }
    
        model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20",generation_config=config)
        response = (model.generate_content(message_send_model)).text.strip()

        return response

    except Exception as e:
        return f"Error : {e}"
        




def extract_text_from_pdf(pdf):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text+=page.extract_text()

    return text

def extract_text_from_voice(voice):
    recognizer = sr.Recognizer()
    with sr.AudioFile(voice) as source:
        audio_data = recognizer.record(source)

    try:
        text =  recognizer.recognize_google(audio_data)
        return text

    except sr.UnknownValueError:
        return "Speech was unintelligible"
    
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    

def text_to_voice(text, lang):

    tts = gTTS(text=text, lang=lang)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes
    