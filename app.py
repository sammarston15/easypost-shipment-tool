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
        # """ SET TEST OR PROD API KEY """
        # if request.form['api_key_type'] == "Production":
        #     easypost.api_key = prod_key 
        # elif request.form['api_key_type'] == "Test":
        easypost.api_key = test_key

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

        if request.form['to_address_street2'] != '':
            ship['to_address']['street2'] = request.form['to_address_street2']
        else:
            ship['to_address']['street2'] = None
        
        if request.form['to_address_residential'] == "true":
            ship['to_address']['residential'] = True

        # print(request.form['parcel_predefined_package'])
        if request.form['parcel_predefined_package'] != '':
            ship['parcel']['length'] = None
            ship['parcel']['height'] = None
            ship['parcel']['width'] = None
            ship['parcel']['predefined_package'] = request.form['parcel_predefined_package']
        else:
            ship['parcel']['predefined_package'] = None


            

        
        try: 
            print(json.dumps(ship, indent=4)) 
            
            shipment = easypost.Shipment.create(ship)
            print(shipment)

            return render_template('rates.html', rate_error_message=shipment.messages,rates=shipment.rates)  

        except:
            return render_template('index.html', error="Oops! There was a problem.")



if __name__ == '__main__':
    app.debug = True
    app.run()