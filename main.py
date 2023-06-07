from flask import Flask, render_template, request
import requests
import openai
import os
from dotenv import load_dotenv

#load openai api key
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

#set up Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Render the index template with the form
     return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get the user's input from the form
    health_condition = request.form['health_condition']
    severity = request.form['severity']
    # Use the OpenAI API to generate a response
    prompt = f"User: I have a {severity} {health_condition}\nChatbot:"
    response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=prompt,
          temperature=0.5,
          max_tokens=60,
          top_p=1,
          frequency_penalty=0,
          stop=["\nUser: ","\nChatbot: "]
    )

    # Extract response from OpenAI API result
    bot_response=response.choices[0].text.strip()

    #Render the template with the response text
    return render_template(
        "response.html",
        user_input=f"I have a {severity} {health_condition}",
        bot_response=bot_response,
    )

# start the Flask app
if __name__ == "__main__":
     app.run(debug=True)


