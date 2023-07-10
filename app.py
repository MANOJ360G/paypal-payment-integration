


# Import External
from flask import Flask, render_template, request
from werkzeug.datastructures import ImmutableOrderedMultiDict
import requests
import time

# Import Local
import dbutil as dbu
import const
from const import (PAYPAL_WEB_BASE, SUBSCRIPTION_AMOUNT, MERCHANT_WEB_BASE, ENV)

app = Flask(__name__)

@app.route('/')
def index_ui():
	try:
		return render_template("index.html")
	except Exception as e:
		return(str(e))

@app.route('/subscription')
def subscription_ui():
	try:

		payment_web_base 		= const.PAYPAL_TESTING_WEB_BASE
		merchant_success_page 	= f"{MERCHANT_WEB_BASE}/payment/success/"
		merchant_cancel_page 	= f"{MERCHANT_WEB_BASE}/payment/cancel/"
		merchant_nofiy_page 	= f"{MERCHANT_WEB_BASE}/payment/notify/"

		merchant_email = const.TESTING_EMAI_ID
		custom_env = "test"

		if(ENV == 'prod'):
			merchant_email 		= const.MERCHANT_EMAIL_ID
			custom_env 			= "live"
			payment_web_base 	= const.PAYPAL_WEB_BASE

		return render_template(
			"subscribe.html",
			payment_web_base 		= payment_web_base,
			merchant_success_page 	= merchant_success_page,
			merchant_cancel_page 	= merchant_cancel_page,
			merchant_nofiy_page 	= merchant_nofiy_page,
			merchant_email			= merchant_email,
			custom_env 				= custom_env
		)
	except Exception as e:
		return(str(e))

@app.route('/payment')
def one_time_payment_ui():
	try:

		payment_web_base 		= const.PAYPAL_TESTING_WEB_BASE
		merchant_success_page 	= f"{MERCHANT_WEB_BASE}/payment/success/"
		merchant_cancel_page 	= f"{MERCHANT_WEB_BASE}/payment/cancel/"
		merchant_nofiy_page 	= f"{MERCHANT_WEB_BASE}/payment/notify/"

		merchant_email = const.TESTING_EMAI_ID
		custom_env = "test"

		if(ENV == 'prod'):
			merchant_email 		= const.MERCHANT_EMAIL_ID
			custom_env 			= "live"
			payment_web_base 	= const.PAYPAL_WEB_BASE

		return render_template(
			"payment.html",
			payment_web_base 		= payment_web_base,
			merchant_success_page 	= merchant_success_page,
			merchant_cancel_page 	= merchant_cancel_page,
			merchant_nofiy_page 	= merchant_nofiy_page,
			merchant_email			= merchant_email,
			custom_env 				= custom_env
		)
	except Exception as e:
		return(str(e))

@app.route('/payment/cancel/')
def cancel_ui():
	try:
		return render_template("cancel.html")
	except Exception as e:
		return(str(e))

@app.route('/payment/success/')
def success():
	try:
		return render_template("success.html")
	except Exception as e:
		return(str(e))

@app.route('/payment/notify',methods=['POST'])
def ipn():
	try:
		
		arguments 						= ''
		request.parameter_storage_class = ImmutableOrderedMultiDict
		values 							= request.form
		
		for xkey, yvalue in values.iteritems():
			arguments += f"&{xkey}={yvalue}"

		validate_url 	= f'{PAYPAL_WEB_BASE}/cgi-bin/webscr?cmd=_notify-validate{arguments}'
		resp 			= requests.get(validate_url)

		if resp.text != 'VERIFIED':

			with open('ipnout.txt','a') as f:
				data = 'FAILURE\n'+str(values)+'\n'
				f.write(data)

			return resp.text

		# success scenario comes here
		try:
			payer_email 	= request.form.get('payer_email')
			unix 			= int(time.time())
			payment_date 	= request.form.get('payment_date')
			username 		= request.form.get('custom')
			last_name 		= request.form.get('last_name')
			payment_gross 	= request.form.get('payment_gross')
			payment_fee 	= request.form.get('payment_fee')
			payment_net 	= float(payment_gross) - float(payment_fee)
			payment_status 	= request.form.get('payment_status')
			txn_id 			= request.form.get('txn_id')
		except Exception as e:
			with open('ipnout.txt','a') as f:
				data = 'ERROR WITH IPN DATA\n'+str(values)+'\n'
				f.write(data)
		
		with open('ipnout.txt','a') as f:
			data = 'SUCCESS\n'+str(values)+'\n'
			f.write(data)

		dbu.add_ipn(
			payer_email,
			unix, 
			payment_date, 
			username, 
			last_name, 
			payment_gross, 
			payment_fee, 
			payment_net, 
			payment_status, 
			txn_id
		)

		return resp.text
	except Exception as e:
		return str(e)

if __name__ == '__main__':

	app.run(
        host 	= "0.0.0.0",
        port 	= 5013,
        debug 	= True
    )