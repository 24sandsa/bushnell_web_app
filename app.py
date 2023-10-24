from flask import Flask
from flask import render_template
from flask import request
from llm_utils import generateResponse

app = Flask(__name__)
chat_history = []

@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def talk():
    user_input = request.form['user_prompt']
    chatbot_response = generateResponse(user_input, persona="Abraham Lincoln")
    chat_history.append({'user': user_input, 'chatbot': chatbot_response})
    return render_template('chat.html',
                            user_input=user_input,
                            chatbot_response=chatbot_response,
                            chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True, port=8080)