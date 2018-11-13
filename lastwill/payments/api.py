import requests

from django.contrib.auth.models import User
from django.db.models import F

from lastwill.payments.models import InternalPayment
from lastwill.profile.models import Profile, UserSiteBalance, SubSite
from lastwill.settings import test_logger
from exchange_API import to_wish, convert


def create_payment(uid, tx, currency, amount, site_id):
    amount = float(amount)
    if amount == 0.0:
        return
    print('create payment')
    user = User.objects.get(id=uid)
    if currency == 'EOSISH':
        value = amount
    elif currency == 'EOS':
        eosish_exchange_rate = float(
            requests.get('https://api.chaince.com/tickers/eosisheos/',
                         headers={'accept-version': 'v1'}).json()['price']
        )
        value = amount / eosish_exchange_rate
    else:
        value = amount if currency == 'WISH' else to_wish(
            currency, amount
        )
    if amount < 0.0:
        negative_payment(user, currency, -value, site_id)
    else:
        positive_payment(user, currency, value, site_id)

    payment = InternalPayment(
        user_id=uid,
        delta=value,
        tx_hash=tx,
        original_currency=currency,
        original_delta=str(amount)
    )
    payment.save()
    print('payment created')


def positive_payment(user, currency, value, site_id):
    if currency in ['EOS', 'EOSISH']:
        Profile.objects.select_for_update().filter(
            id=user.profile.id).update(
            eos_balance=F('eos_balance') + value)
    else:
        Profile.objects.select_for_update().filter(
            id=user.profile.id).update(
            balance=F('balance') + value)


def negative_payment(user, currency, value, site_id):
    if currency not in ['EOS', 'EOSISH']:

        if not Profile.objects.select_for_update().filter(
                user=user, balance__gte=value
        ).update(balance=F('balance') - value):
            raise Exception('no money')
    else:
        eos_cost = value
        if not Profile.objects.select_for_update().filter(
                user=user, eos_balance__gte=eos_cost
        ).update(eos_balance=F('eos_balance') - eos_cost):
            raise Exception('no money')
