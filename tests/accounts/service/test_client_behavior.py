import pytest
from GetSequenceIoApiClient.client import SequenceApiClient, SequenceApiError, SequenceAuthError
from GetSequenceIoApiClient import models
from tests._dummy_client import DummyResponse, DummySession


@pytest.mark.asyncio
async def test_async_get_accounts_success():
    accounts_data = {"data": {"accounts": []}}
    dummy_response = DummyResponse(200, accounts_data)
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "test-token")
    result = await client.accounts.async_get_accounts()
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_async_get_accounts_auth_error():
    dummy_response = DummyResponse(401, {})
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "bad-token")
    with pytest.raises(SequenceAuthError):
        await client.accounts.async_get_accounts()


@pytest.mark.asyncio
async def test_async_get_accounts_api_error():
    dummy_response = DummyResponse(500, {})
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "test-token")
    with pytest.raises(SequenceApiError):
        await client.accounts.async_get_accounts()


@pytest.mark.asyncio
async def test_async_test_connection_success():
    accounts_data = {"data": {"accounts": []}}
    dummy_response = DummyResponse(200, accounts_data)
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "test-token")
    assert await client.accounts.async_test_connection() is True


@pytest.mark.asyncio
async def test_async_test_connection_failure():
    dummy_response = DummyResponse(401, {})
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "bad-token")
    assert await client.accounts.async_test_connection() is False


@pytest.mark.asyncio
async def test_async_get_account_and_models():
    account_payload = {
        "id": "a1",
        "name": "Acct",
        "type": "POD",
        "balance": {"balanceInCents": 12345, "error": None},
    }
    dummy_response = DummyResponse(200, account_payload)
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "token")
    acct = await client.accounts.async_get_account("a1")
    assert isinstance(acct, models.Account)
    assert acct.balance.balance_in_cents == 12345
