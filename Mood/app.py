from flask import Flask, request, redirect , render_template
from decouple import config
import openai
from openai import error as openai_error
import requests

#Please visit the .env file to add your api key
openai.api_key =  config('OPENAI_API_KEY') or ""

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return "Hello World"



@app.route('/', methods=['GET'])
def main_page():
    return render_template('index.html')



@app.route('/analyze' , methods=['GET','POST'])
def analyze_text():
    if request.method == 'POST':
        user_text = request.form['text']
        try:
            mood = analyze_mood(user_text)
            return f"The mood of the text is: {mood}</br></br><a href='/'>Go back</a>"
        except openai_error.OpenAIError as e:
            return f"OpenAI API Error: {str(e)}</br></br><a href='/'>Go back</a>"
        except requests.exceptions.RequestException as e:
            return f"Request Error: {str(e)}</br></br><a href='/'>Go back</a>"
    else:
        return redirect('/')



def analyze_mood(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    )
    print(response)
    sentiment = response['choices'][0]['message']['content'].strip().lower()
    print(sentiment)
    if "congratulations" in sentiment:
        return "Positive Mood"
    elif "sorry"  in sentiment:
        return "Negative Mood"
    else:
        if any(word in sentiment for word in ["happy", "joyful", "excited","great","proud","wonderful","beautiful"]):
            return "Positive Mood"
        elif any(word in sentiment for word in ["sad", "unhappy", "angry","dissapointing"]):
            return "Negative Mood"
        else:
            return "Neutral Mood"


# **Experimenting**
# """
#         <form method="POST" action="/analyze">
#             <label for="text">Enter text for mood analysis:</label>
#             </br>
#             </br>
#             <textarea id="text" name="text" rows="4" cols="50"></textarea>
#             </br>
#             </br>
#             <input type="submit" value="Submit">
#         </form>
#"""




if __name__ == '__main__':
    app.run(debug=True)



