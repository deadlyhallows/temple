""" The django version is 1.5.1 the imported function mauy varing depands on the versions"""
import json, datetime, hashlib
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from payu_biz.payu_config import (merchant_key, mode,su_url, fu_url, cu_url)
from payu_biz.payubiz import PayuBizTransactions as PayBz
from payu_biz.payubiz import PayuPaymentTrasactionService as PayWTS
from django.shortcuts import render

def make_transaction(request):
    #payu_biz = PayBz()
    #action = "makepayment"
    #validate_data = payu_biz.validate_request_params(action, data)
    #transaction_dict = data.copy()
    #phone_no = data.pop('phone')
    #data['key'] = merchant_key
    #hash_code = payu_biz.generate_payment_hash(data)
    #payment_url = payu_biz.generate_payment_url()
    #firstname = transaction_dict['firstname']
    #surl,furl,curl = su_url, fu_url, cu_url
    return render(request, 'orders/order/create.html')
         
            

@csrf_exempt
def payu_success(request):
    """ we are in the payu success mode"""
    return HttpResponse(json.dumps(request.POST),mimetype='application/json')
    
@csrf_exempt
def payu_failure(request):
    """ We are in payu failure mode"""
    return HttpResponse(json.dumps(request.POST),mimetype='application/json')

@csrf_exempt
def payu_cancel(request):
    """ We are in the Payu cancel mode"""
    return HttpResponse(json.dumps(request.POST),mimetype='application/json')

def verify_payment(txnid):
    v_p = PayWTS()
    vp_p = v_p.verify_payment(txnid)
    return vp_p

def check_payment(mihpayid):
    c_p = PayWTS()
    cp_p = c_p.check_payment(mihpayid)
    return cp_p

def capture_transaction(mihpayid):
    c_t = PayWTS()
    ct_t = c_t.capture_transaction(mihpayid)
    return ct_t

def cancel_transaction(mihpayid, amount):
    c_t = PayWTS()
    ct_t = c_t.cancel_transaction(mihpayid, amount)
    return ct_t


def refund_transaction(mihpayid, amount):
    r_t = PayWTS()
    rt_t = r_t.refund_transaction(mihpayid, amount)
    return rt_t

def cancel_refund_transaction(mihpayid, amount):
    cr_t = PayWTS()
    cr_rt = cr_t.cancel_refund_transaction(mihpayid, amount)
    return cr_rt

def check_action_status(request_id):
    ca_s = PayWTS()
    ca_sd = ca_s.check_action_status(request_id)
    return ca_sd

from hashlib import sha512
from django.conf import settings
KEYS = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
        'udf1', 'udf2', 'udf3', 'udf4', 'udf5',  'udf6',  'udf7', 'udf8',
        'udf9',  'udf10')

def generate_hash(data):
    keys = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
            'udf1', 'udf2', 'udf3', 'udf4', 'udf5',  'udf6',  'udf7', 'udf8',
            'udf9',  'udf10')
    hash = sha512('')
    for key in KEYS:
        hash.update("%s%s" % (str(data.get(key, '')), '|'))
    hash.update(settings.PAYU_INFO.get('merchant_salt'))
    return hash.hexdigest().lower()

def verify_hash(data, SALT):
    keys = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
            'udf1', 'udf2', 'udf3', 'udf4', 'udf5',  'udf6',  'udf7', 'udf8',
            'udf9',  'udf10')
    keys.reverse()
    hash = sha512(settings.PAYU_INFO.get('merchant_salt'))
    hash.update("%s%s" % ('|', str(data.get('status', ''))))
    for key in KEYS:
        hash.update("%s%s" % ('|', str(data.get(key, ''))))
    return (hash.hexdigest().lower() == data.get('hash'))    




