from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/domains/tlds', methods=['GET'])
def get_tlds():
    return jsonify(open('tlds.json').read())	

if __name__ == '__main__':
    app.run(debug=True)
