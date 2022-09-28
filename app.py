from flask import Flask, render_template, request
import easypost
import os
import json



""" LOAD TEST AND PROD API KEY """
test_key = os.getenv('TEST_KEY')




app = Flask(__name__)


# home page
@app.route('/') 
def index():
    return render_template('index.html')


# handle form data
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':

        # set the API key in the client library
        easypost.api_key = test_key

        # create shipment dictionary using info sent from the client
        ship = {
            "to_address": {
                "name": request.form['to_address_name'],
                "street1": request.form['to_address_street1'],
                "city": request.form['to_address_city'],
                "state": request.form['to_address_state'],
                "zip": request.form['to_address_zip'],
                "country": request.form['to_address_country'],
                "phone": request.form['to_address_phone'],
                "email": request.form['to_address_email'],
            },
            "from_address": {
                "name": request.form['from_address_name'],
                "street1": request.form['from_address_street1'],
                "city": request.form['from_address_city'],
                "state": request.form['from_address_state'],
                "zip": request.form['from_address_zip'],
                "country": request.form['from_address_country'],
                "phone": request.form['from_address_phone'],
                "email": request.form['from_address_email']
            },
            "parcel": {
                "length": request.form['parcel_length'],
                "width": request.form['parcel_width'],
                "height": request.form['parcel_height'],
                "weight": request.form['parcel_weight'],
            },
        }

        # check to see if street2 was provided
        if request.form['to_address_street2'] != '':
            ship['to_address']['street2'] = request.form['to_address_street2']
        else:
            ship['to_address']['street2'] = None
        
        # check if to_address.residential is true
        if request.form['to_address_residential'] == "true":
            ship['to_address']['residential'] = True
        else:
            ship['to_address']['residential'] = False

        # remove provided dims if a predefined_package was included
        if request.form['parcel_predefined_package'] != '':
            ship['parcel']['length'] = None
            ship['parcel']['height'] = None
            ship['parcel']['width'] = None
            ship['parcel']['predefined_package'] = request.form['parcel_predefined_package']
        else:
            ship['parcel']['predefined_package'] = None

        # create the shipment and fetch rates from EasyPost
        try: 
            print('hit try block')
            print(json.dumps(ship, indent=4)) 
            
            shipment = easypost.Shipment.create(
                to_address=ship['to_address'],
                from_address=ship['from_address'],
                parcel=ship['parcel']
            )
            print(shipment)

            # sort rates by `carrier` before sending them to the client
            def sorted_rates(e):
                return e['carrier']

            shipment.rates.sort(key=sorted_rates)

            # if the above is successful, render the rates.html template
            return render_template('rates.html', rate_error_message=shipment.messages,rates=shipment.rates)  

        except Exception as e:
            print(e)
            # render the index.html template but with an alert at the top with the Exception
            return render_template('index.html', error=f"Oops! There was a problem: {e}")



if __name__ == '__main__':
    app.debug = True
    app.run()