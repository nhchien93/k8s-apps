import os

from flask import Flask, jsonify, request

import ask_gemini

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome To Home Page'


@app.route('/hello/<name>')
def hello(name):
    return jsonify(message=f'Welcome {name}!')


@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify(received=data)


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data['question']
    gemini_response = ask_gemini.ask(question)

    response = {
        "question": question,
        "answer": gemini_response.text,
        "token_count": {
            "prompt_tokens": gemini_response.usage_metadata.prompt_token_count,
            "total_tokens": gemini_response.usage_metadata.total_token_count
        }
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv('APP_PORT'), debug=True)
