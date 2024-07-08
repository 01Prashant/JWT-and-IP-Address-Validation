from flask import Flask, render_template, request, jsonify
import jwt
import datetime

app = Flask("__main__")
app.config['SECRET_KEY'] = '412e1fbc4b5fcefc7c8d6e15a301b430ee0ecd376594b674'

@app.route('/')
def home():
    return render_template('home.html')

# Generate JWT Token
@app.route('/generate-token', methods=['GET'])
def generate_token():
    ip_address = request.remote_addr
    payload = {
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=30),
        'sub': ip_address
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})

# Validate JWT Token and IP Address
@app.route('/validate', methods=['POST'])
def validate():
    token = request.form.get('token_input')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 400
    
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        ip_address = request.remote_addr
        if decoded['sub'] != ip_address:
            return jsonify({'message': 'Invalid IP address!'}), 400
        return jsonify({'message': 'Token and IP address are valid!'})
    except jwt.ExpiredSignatureError as e:
        print(f"Token has expired: {str(e)}")
        return jsonify({'message': 'Token has expired!'}), 400
    except jwt.InvalidTokenError as e:
        print(f"Invalid token!: {str(e)}")
        return jsonify({'message': 'Invalid token!'}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")