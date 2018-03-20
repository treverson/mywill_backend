from lastwill.settings import *

import unittest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient

factory = APIClient()

test_user = User.objects.first()

class TestReceiver(unittest.TestCase):
    def test_get_cost(self):
        request = factory.get('/api/get_cost/', {
            'contract_type': '2',
            'heirs_num': 5,
            'heirs': 100,
            'active_to': 145009888877
        }, format='json')
        assert(request.status_code==200)

    def test_balance(self):
        request = factory.get('/api/balance/', {
            'address': 'dhjbasdbhaabhchbha',
        }, format='json')
        assert(request.status_code==200)

    def test_get_code(self):
        request = factory.get('/api/get_code/', {
            'contract_type': 2,
        }, format='json')
        assert(request.status_code==200)

    def test_test_comp(self):
        request = factory.get('/api/test_comp/', {
            'id': 1,
        }, format='json')
        assert(request.status_code==200)

    def test_get_contract_type(self):
        request = factory.get('/api/get_contract_types/', {
            'id': 1,
        }, format='json')
        assert(request.status_code==200)

    # def test_eth2rub(self):
    #     request = factory.get('/api/eth2rub/')
    #     assert(request.status_code== 200)

    def test_deploy(self):
        request = factory.get('/api/deploy/', {
            'id': 1, 'user': test_user
        }, format='json')
        assert(request.status_code, 200)

    def test_get_token_contracts(self):
        request = factory.get('/api/get_token_contracts/', {
            'user': test_user
        }, format='json')
        assert(request.status_code==200)

    def test_get_statistics(self):
        request = factory.get('/api/get_statistics/')
        assert(request.status_code==200)

    def test_get_contracts(self):
        request = factory.get('/api/contracts')
        assert(request.status_code==200)

    def test_get_sentences(self):
        request = factory.get('/api/sentences')
        assert(request.status_code==200)

    def test_post_contracts(self):
        request = factory.post('/api/contracts', {
            'user_id': test_user.id,
            'owner_address': 'dsasdadsa',
            'cost': 100,
            'balance': 300,
            'name': 'scacsc',
            'contract_type': 3
        })
        assert(request.status_code==200)

    def test_post_sentences(self):
        request = factory.post('/api/sentences', {
            'username': test_user.username,
            'email': test_user.email,
            'contract_name': 'sdcscs',
            'message': 'czsdcsdsdc'
        })
        assert(request.status_code==200)
