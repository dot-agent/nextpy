# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import os
from openai import OpenAI
import nextpy as xt 
from .state import State, QA
import speech_recognition as sr

r = sr.Recognizer()

from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key = os.environ["OPENAI_API_KEY"]
)

INTERVIEW_DEFAULT = {
    "Interview": [],
}

class InterviewState(State):
    # Job Description 
    job_desc: str = ''

    interview_chat: str = "Interview"

    index : dict[str, int] = { interview_chat:0 }

    # A dict from the chat name to the list of questions and answers.
    interview_chats: dict[str, list[QA]] = INTERVIEW_DEFAULT

    interview_option: str = 'visible'

    interview_convo: str = 'none'

    interview_answer: str = ''

    interview_processing: bool = False

    interview_prompt = ''

    recording: bool = False 

    text = ''

    def start_recording(self):
        self.recording = True
        self.interview_answer = 'Listening ........'
        yield
        with sr.Microphone() as source:
            audio = r.listen(source)
            self.interview_answer = ''
            try:
                self.text += r.recognize_google(audio)
            except:
                print("Google Speech Recognition could not understand audio")
        self.interview_answer = self.text 
        self.recording = False
        yield 

    async def process_interview(self, form_data: dict[str, str]=None):
        if self.interview_option == 'visible':
            self.interview_option = 'none'
            self.interview_convo = 'visible'
            self.interview_prompt = f'''
                Your name is NextpyGPT and you are a professional interviewer chatbot.
                Your task is to ask questions one by one based on the given Job description or Role -  
                JOB DESCRIPTION = Role = {self.job_desc}

                Always remeber the flow of conversation given in points below - 
                1) Start with basic question like name and introduction.
                2) Initially ask basic questions related to the given Job description or Role and slowly increase the difficulty
                3) Ask 10-15 questions one by one and at the end ask if user wants to stop
                4) Anytime the user says to end interview give them a genuine conclusion for their performance based on the interview in a good tone only.
                5) At the end just respond politely if user wants to restart
            '''
            self.messages = [
                {"role": "system", "content": self.interview_prompt}
            ]
            self.interview_processing = True
            self.interview_answer = ""
            self.text = ''
            yield

            # Start a new session to answer the question.
            session = client.chat.completions.create(
                model=os.getenv("OPENAI_API_MODEL"),
                messages=self.messages,
                stream=True,
            )

            qa = QA(question="", answer="", index=self.index[self.interview_chat])
            self.index[self.interview_chat] += 1
            self.interview_chats[self.interview_chat].append(qa)
            yield

            # Stream the results, yielding after every word.
            for item in session:
                if hasattr(item.choices[0].delta, "content"):
                    question_text = item.choices[0].delta.content
                    if question_text is None :
                        question_text = ''
                    self.interview_chats[self.interview_chat][-1].question += question_text
                    self.interview_chats = self.interview_chats
                    yield

            # Toggle the processing flag.
            self.interview_processing = False

            return
        

        self.interview_chats[self.interview_chat][-1].answer = self.interview_answer
        question = self.interview_chats[self.interview_chat][-1].question
        self.messages.append({"role": "assistant", "content": question})
        self.messages.append({"role": "user", "content": self.interview_answer})
        
        # Clear the input and start the processing.
        self.interview_processing = True
        self.interview_answer = ""
        yield

        # Start a new session to answer the question.
        session = client.chat.completions.create(
            model=os.getenv("OPENAI_API_MODEL"),
            messages=self.messages,
            stream=True,
        )

        qa = QA(question="", answer="", index=self.index[self.interview_chat])
        self.index[self.interview_chat] += 1
        self.interview_chats[self.interview_chat].append(qa)

        # Stream the results, yielding after every word.
        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                question_text = item.choices[0].delta.content
                if question_text is None :
                    question_text = ''
                self.interview_chats[self.interview_chat][-1].question += question_text
                self.interview_chats = self.interview_chats
                yield

        # Toggle the processing flag.
        self.interview_processing = False