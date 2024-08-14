from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["7 per minute"],
    storage_uri="memory://",
)

@app.route('/')
@limiter.exempt
def home():
    return render_template('index.html')

@app.route('/tlds', methods=['GET'])
@limiter.exempt
def get_tlds():
    return open('tlds.json').read()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
