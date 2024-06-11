import gradio as gr
import vertexai
from vertexai.generative_models import GenerativeModel
import os
import time

# app = Flask(__name__)
PROJECT_ID = "lbplc-reboot24lon-974"  
LOCATION = "europe-west2"  

vertexai.init(project=PROJECT_ID, location=LOCATION)

def create_session():
    model = GenerativeModel(
        model_name="gemini-1.5-pro-001",
        system_instruction=[
            "You are a chatbot for Lloyds Bank, helping customers to set up trusted roles for their banking accounts. There are a range of these roles, described below:",
            """
Temporary account control: Full account control for a limited period.
Temporary payments access: Can make payments for a set period.
Palliative care service: Manages finances for medical and daily care needs.
Dementia care service: Oversees transactions and bill payments for someone with dementia.
Transaction double checking: Approves all transactions before completion.
Limited cash card access: Restricted access to withdraw funds or make purchases up to a limit.""",
            "You will follow these steps: Firstly, ask the customer for the nominee's first name, surname, email, phone number and address.",
            "Next, you will ask them to describe the problem and what accesses they would like to grant. You will suggest one of the roles above.",
            "Finally, you will ask them which revalidation period they would like: 3, 6 or 12 months."
        ]
        )
    return model.start_chat()

chat = create_session()

def transform_history(history):
    new_history = []
    for chat in history:
        new_history.append({"parts": [{"text": chat[0]}], "role": "user"})
        new_history.append({"parts": [{"text": chat[1]}], "role": "model"})
    return new_history

def response(message, history):
    global chat
    # The history will be the same as in Gradio, the 'Undo' and 'Clear' buttons will work correctly.
    chat.history = transform_history(history)
    response = chat.send_message(message)
    response.resolve()

    # Each character of the answer is displayed
    for i in range(len(response.text)):
        time.sleep(0.01)
        yield response.text[: i+1]


if __name__ == '__main__':
    gr.ChatInterface(response,
                    title='Trusted Person Setup Chatbot',
                    textbox=gr.Textbox(placeholder="Question"),
                    retry_btn=None,
                    server_name="0.0.0.0",
                    server_port=8080).launch(debug=True)
