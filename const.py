


import os
from dotenv import load_dotenv

load_dotenv()

PAYPAL_WEB_BASE                 = os.getenv('PAYPAL_WEB_BASE')
PAYPAL_TESTING_WEB_BASE         = os.getenv('PAYPAL_TESTING_WEB_BASE')
SUBSCRIPTION_AMOUNT             = os.getenv('SUBSCRIPTION_AMOUNT')
MERCHANT_WEB_BASE               = os.getenv('MERCHANT_WEB_BASE')
MERCHANT_EMAIL_ID               = os.getenv('MERCHANT_EMAIL_ID')
TESTING_EMAI_ID                 = os.getenv('TESTING_EMAI_ID')
ENV                             = os.getenv('ENV')

