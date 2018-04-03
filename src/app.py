from flask import Flask, request
from zatiq_businesses_mysql_client import ZatiqBusinessesMySQLClient
from zatiq_users_mysql_client import ZatiqUsersMySQLClient
app = Flask(__name__)

@app.route('/')
def hello_world():
    return('Hello World!')

@app.route('/businesses/list/')
def test_get_first_business():
    zatiq_businesess = ZatiqBusinessesMySQLClient()
    response = zatiq_businesess.get_all_businesses()
    return(response)

@app.route('/users/list/')
def test_get_first_user():
    zatiq_users = ZatiqUsersMySQLClient()
    response = zatiq_users.get_all_users()
    return(response)

@app.route('/user/login/', methods=['POST'])
def login_as_user():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMySQLClient()
        print(request.form)
        user_auth_token = request.form.get('accessToken')
        login_method = request.form.get('method')
        response = zatiq_users.user_register(user_auth_token, login_method)
        return(response)

