from flask import Flask, request, jsonify, render_template, redirect
import pickle
import firebase_admin
from firebase_admin import credentials, auth
from sklearn.ensemble import RandomForestRegressor


app = Flask(__name__)
cred = credentials.Certificate("zenzephyr-ab6b5-firebase-adminsdk-a9pxu-c1600c1b01.json")
firebase_admin.initialize_app(cred)

@app.route('/')
def index():
    return render_template('login.html')
@app.route('/index')
def Usermanage():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username and password are correct
        if username == 'admin' and password == '1234':
            return redirect('/index')  # Redirect to index page

        # If username or password is incorrect, show an error message
        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/user_list')
def user_list():
    users = auth.list_users()
    user_list = [{'uid': user.uid, 'email': user.email} for user in users.users]
    return jsonify(user_list)



@app.route('/register', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')
    user = auth.create_user(email=email, password=password)
    return jsonify({'uid': user.uid})


@app.route('/login', methods=['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')
    user = auth.get_user_by_email(email)
    return jsonify({'uid': user.uid})


@app.route('/update_user', methods=['POST'])
def update_user():
    user_uid = request.form.get('uid')
    new_display_name = request.form.get('new_display_name')
    new_email = request.form.get('new_email')

    user = auth.update_user(
        user_uid,
        display_name=new_display_name,
        email=new_email
    )

    response = jsonify({'message': 'User information updated successfully'})

    # Add JavaScript to show an alert after the response is received.
    response.headers.add('alert', 'alert("User information updated successfully");')

    return response
    

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_uid = request.form.get('uid')
    auth.delete_user(user_uid)
    response1 = jsonify({'message': 'User deleted successfully'})
    response1.headers.add('alert', 'alert("User deleted successfully");')

    return response1



# Load the pre-trained model
with open('random_forest_model1 (1).pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        responses = request.form['responses'].split(',')
        responses = [int(response) for response in responses]

        # Make prediction
        predicted_value = loaded_model.predict([responses])
        return jsonify({'prediction': int(predicted_value[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
