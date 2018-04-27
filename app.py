from flask import Flask, request


app = Flask(__name__)

@app.route('/', methods=['POST'])
def result():
    text = request.form['story'] # should display 'bar'
    print(text)
    return 'Received !' # response to your request.

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)