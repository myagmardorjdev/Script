from flask import *
path = 'C:/Users/myagmardorj/Git/lesson3/barcode_printer/'


app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('about.html')

@app.route('/button_clicked', methods=['POST'])
def button_clicked():
    user_input = request.form.get('user_input')
    baraaner = request.form.get('second_input')
    print(user_input)
    print(baraaner)
    print(f"Button clicked with user input: {user_input}")
    return f"Button clicked with user input: {user_input}"

if __name__ == '__main__':
    app.run(debug=True)
