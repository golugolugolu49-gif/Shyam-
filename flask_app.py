from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    data = request.get_json()
    message = data.get('message')
    
    # Simulate a response from ChatGPT tool
    response = f"ChatGPT response to: {message}"
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)