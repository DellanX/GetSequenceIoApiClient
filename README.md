# GetSequenceIoApiClient

A Python client for the Sequence financial orchestration platform API.

## Features
- Async API access to Sequence accounts
- Pod, Income Source, Liability, Investment, and External account helpers
- Pydantic-backed typed models for request/response validation
- Modular REST resources (`accounts`, `rules`, `activity`, `audit_logs`)
- Designed for integration with Home Assistant and other Python apps

## Installation
```bash
pip install GetSequenceIoApiClient
```

## Usage
```python
import aiohttp
from GetSequenceIoApiClient import SequenceApiClient, SequenceClientConfig

async def main():
    async with aiohttp.ClientSession() as session:
        client = SequenceApiClient(
            session,
            "YOUR_ACCESS_TOKEN",
            config=SequenceClientConfig(
                base_url="https://api.getsequence.io/platform/v1",
                timeout_seconds=30,
            ),
        )
        accounts = await client.accounts.async_get_accounts()
        first = accounts[0]
        print(first.id, first.type)
```

## Model parsing behavior

All schemas are Pydantic models and support both camelCase (API-native) and
snake_case (Pythonic) keys during parsing:

```python
from GetSequenceIoApiClient.models import Account

account = Account.from_dict({"id": "a1", "type": "POD", "createdAt": "..."})
payload = account.to_dict()  # camelCase for outbound JSON
```

Rule models are now strongly typed as well (`Trigger`, `RuleStep`,
`RuleAction`, `RuleCondition`, `TriggerDetails`) instead of generic maps.

## Author
Dyllan Macias (@DellanX)

## License
See LICENSE file.
