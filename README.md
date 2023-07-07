# Async API wrapper for smspva

## Installation

```bash
pip install git+https://github.com/optinsoft/asmspva.git
```

## Usage

```python
from asmspva import AsyncSmsPva
import asyncio

async def test(apiKey: str):
    asmspva = AsyncSmsPva(apiKey)
    print("getBalance\n", await asmspva.getBalance('opt4'))    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test('PUT_YOUR_API_KEY_HERE'))
```
