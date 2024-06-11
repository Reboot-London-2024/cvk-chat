from flask import Flask, render_template, request, jsonify
import vertexai
from vertexai.generative_models import GenerativeModel
import os

app = Flask(__name__)
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


def response(chat, message):
    parameters = {
        "temperature": 0.2,
    }
    text_response = []
    responses = chat.send_message(message, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/palm2', methods=['GET', 'POST'])
def vertex_palm():
    user_input = ""
    if request.method == 'GET':
        user_input = request.args.get('user_input')
    else:
        user_input = request.form['user_input']
    chat_model = create_session()
    content = response(chat_model,user_input)
    return jsonify(content=content)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
