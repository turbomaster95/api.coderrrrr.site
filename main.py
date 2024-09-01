from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import hashlib

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["7 per minute"],
    storage_uri="memory://",
)

def md5(fname):
    with open(fname, "rb") as file:
        return hashlib.md5(file.read()).hexdigest()  # Changed to read the entire file

def increment_version(version):
    major, minor, patch = map(int, version.split('.'))
    patch += 1
    return f"{major}.{minor}.{patch}"

current_hash = md5(__file__)

try:
    with open('data/md5.txt', 'r') as f:
        previous_hash = f.read().strip()
except FileNotFoundError:
    previous_hash = ''

if current_hash != previous_hash:
    try:
        with open('data/ver.txt', 'r') as f:
            oldver = f.read().strip()
    except FileNotFoundError:
        oldver = '0.0.0'
    
    new_version = increment_version(oldver)
    
    with open('data/ver.txt', 'w') as f:
        f.write(new_version)
    
    with open('data/md5.txt', 'w') as f:
        f.write(current_hash)
else:
    with open('data/ver.txt', 'r') as f:
        new_version = f.read().strip()


@app.route('/')
@limiter.exempt
def home():
    return render_template('index.html', version=new_version)

@app.route('/tlds', methods=['GET'])
@limiter.exempt
def get_tlds():
    return open('data/tlds.json').read()

@app.route('/domains')
@limiter.exempt
def get_domains():
    return open('data/domains.json').read()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
