# import pytest
#
# from httpx import AsyncClient
# from fastapi.testclient import TestClient
#
# from wallet_service.app import app
# from wallet_service.utils import session
# from wallet_service.repository import WalletRepository
#
# @session
# async def session_wrapper(a_session, coroutine):
#
# client = TestClient(app)
#
#
# # def test_valid_create_user():
# #     response = client.post(
# #         '/v1/users',
# #         json={'username': 'test'}
# #     )
# #
# #     assert response.status_code == 201
# #     assert response.json() == {
# #         "user": {
# #             "id": 0,
# #             "username": "test"
# #         },
# #         "wallet": {
# #             "id": 0,
# #             "balance": 0
# #         }
# #     }
# #
# #
# # def test_invalid_create_user():
# #     response = client.post(
# #         '/v1/users',
# #         json={'username_invalid': 'invalid'}
# #     )
# #     assert response.status_code == 422
#
#
# def test_wallet_pop_up_positive_amount():
#     response = client.put(
#         '/v1/wallets/pop-up',
#         json={'wallet_id': 0, 'amount': '123.123'}
#     )
#     assert response.status_code == 200
#
#
# def test_wallet_pop_up_negative_amount():
#     response = client.put(
#         '/v1/wallets/pop-up',
#         json={'wallet_id': 0, 'amount': '-123.123'}
#     )
#     assert response.status_code == 402
#
#
# def test_invalid_wallet_pop_up():
#     response = client.put(
#         '/v1/wallets/pop-up',
#         json={'wallet_id': 999, 'amount': '123.123'}
#     )
#     assert response.status_code == 404
#
#
# def test_wallet_pop_up_balance_precision():
#     # reset balance
#     response = None
#
#     for _ in range(3):
#         response = client.put(
#             '/v1/wallets/pop-up',
#             json={'wallet_id': 0, 'amount': '0.1'}
#         )
#
#     assert response is not None
#     assert response.json().get('balance') == 0.3
#     # check balance by repository
#
#
# # TODO write 3 types of tests for every api
# #  1. success
# #  2. failure
# #  3. valid precision data
