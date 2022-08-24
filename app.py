from flask import Flask, render_template, request


app = Flask(__name__)


# home page
@app.route('/') 
def index():
    return render_template('index.html')

# handle form data
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        if customer == '':
            return render_template('index.html', error="Please enter required fields.")
        else:
            return render_template('index.html', success="Success!")


if __name__ == '__main__':
    app.debug = True
    app.run()