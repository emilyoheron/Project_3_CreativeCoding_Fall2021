from flask import Flask, render_template, jsonify
import random
import requests
import json
import RPi.GPIO as GPIO
list1 = [60, 62, 65, 70, 72, 75, 77, 80, 82, 85, 87, 90, 92, 95, 97, 100]

app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
pulse = 24
pulseSts = GPIO.LOW

GPIO.setup(pulse, GPIO.IN)

@app.route("/")
def index():
    y = random.choice(list1)
    x = 0
    heart = 0
    while x < y:
        pulseSts = GPIO.input(pulse)
        heart += pulseSts
        x += 1
    templateData = {
      'title' : 'GPIO input Status!',
      'pulse'  : heart,
    }

    return render_template('index.html', **templateData)

@app.route('/hello', methods=['POST'])
def hello():
    month = request.form['month']
    day = request.form['day']
    year = request.form['year']

url = "https://astronomy.p.rapidapi.com/api/v2/studio/moon-phase"

payload = "{\n    \"format\": \"png\",\n    \"observer\": {\n        \"date\": \"2001-24-07\",\n        \"latitude\": 6.7898,\n        \"longitude\": {{pulse}}\n    },\n    \"style\": {\n        \"backgroundColor\": \"red\",\n        \"backgroundStyle\": \"stars\",\n        \"headingColor\": \"white\",\n        \"moonStyle\": \"sketch\",\n        \"textColor\": \"red\"\n    },\n    \"view\": {\n        \"type\": \"portrait-simple\"\n    }\n}"
headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "astronomy.p.rapidapi.com",
    'x-rapidapi-key': "fe7da5001emsh706d6f1899ef5fcp178585jsn16ec6fb78ade"
    }

response = requests.request("POST", url, data=payload, headers=headers)

obj = response.json()
image = obj['data']['imageUrl']

@app.route('/moon')
def moonPhase():
    ##return render_template('index.html', variable = image )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)