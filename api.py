from sys import meta_path
from flask import Flask, request
import json 

app = Flask(__name__)


@app.route('/recommend', methods=['GET', 'POST'])
def api():
    key_word = ""
    if request.method == 'POST':
        key_word = request.json['search']
    elif request.method == 'GET':
        key_word = request.args.get("search")

    
    
    return key_word 

if __name__ == '__main__':
    print("Hello World")
    app.run(host="0.0.0.0", port=8008)
