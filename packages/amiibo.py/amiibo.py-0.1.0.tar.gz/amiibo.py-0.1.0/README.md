# amiibo.py

A powerfull, rich API Wrapper for amiiboapi.com

## Features

* 100% API Coverage
* Async/Sync versions
* Optimized speed

## Installation

Note: Python 3.5.3 or higher is requires

Install stable version:
```
# if your os is macOS
> python3 -m pip install -U amiibo.py
# If your os is Windows
> py -3 -m pip install -U amiibo.py
```

Install development version:
```
> git clone https://github.com/XiehCanCode/amiibo.py
> cd amiibo.py
> python3 -m pip install .
```

## Usage

A Quick example in Sync version:
```py
import amiibo

client = amiibo.Client()
print(client.get_amiibos())
```

A Quick example in Async version:
```py
import asyncio
import amiibo

def main():
    client = amiibo.AsyncClient()
    print(await client.get_amiibos())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```