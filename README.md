# Remnawave Python SDK

> [!WARNING]
> This repository is a fork of the official SDK [`remnawave/python-sdk`](https://github.com/remnawave/python-sdk).

[![Stars](https://img.shields.io/github/stars/remnashop/remnapy.svg?style=social)](https://github.com/remnashop/remnapy/stargazers)
[![Forks](https://img.shields.io/github/forks/remnashop/remnapy.svg?style=social)](https://github.com/remnashop/remnapy/network/members)
[![Issues](https://img.shields.io/github/issues/remnashop/remnapy.svg)](https://github.com/remnashop/remnapy/issues)
[![Supported python versions](https://img.shields.io/pypi/pyversions/remnapy.svg)](https://pypi.python.org/pypi/remnapy)
[![Downloads](https://img.shields.io/pypi/dm/remnapy.svg)](https://pypi.python.org/pypi/remnapy)
[![PyPi Package Version](https://img.shields.io/pypi/v/remnapy)](https://pypi.python.org/pypi/remnapy)

A Python SDK client for interacting with the **[Remnawave API](https://docs.rw/)**.
This library simplifies working with the API by providing convenient controllers, Pydantic models for requests and responses, and fast serialization with `orjson`. 

## 📦 Installation

### Production Version
Install the latest release from PyPI:

```bash
pip install remnapy
```

Pin the version to the panel line you run:

```toml
# pyproject.toml
dependencies = ["remnapy (>=3.2.1, <3.3.0)"]
```

### Development Version
If you need the unreleased code from the `development` branch:

```bash
pip install git+https://github.com/remnashop/remnapy.git@development
```

---

## 🫥 Compatible versions

The package version mirrors the Remnawave panel version exactly — `remnapy` **3.2.1** targets Remnawave **3.2.1**.

| Package Version | Remnawave Panel Version |
| --------------- | ----------------------- |
| 3.2.1           | >=3.2.1, <3.3.0         |

### Dependencies
- `rapid-api-client` (==0.6.0)
- `orjson` (>=3.10.15, <4.0.0)
- `httpx` (>=0.27.2, <0.28.0)
- `pydantic[email]` (>=2.9.2, <3.0.0)
- `pydantic-core` (>=2.33.1, <2.34.0)
- `cryptography` (>=46.0.3, <47.0.0)

## 🚀 Usage

Here’s a quick example to get you started:

```python
import os
import asyncio

from remnapy import RemnawaveSDK
from remnapy.models import (
    UsersResponseDto, 
    UserResponseDto,
    GetAllConfigProfilesResponseDto,
    CreateInternalSquadRequestDto
)

async def main():
    # URL to your panel (ex. https://vpn.com or http://127.0.0.1:3000)
    base_url: str = os.getenv("REMNAWAVE_BASE_URL")
    # Bearer Token from panel (section: API Tokens) 
    token: str = os.getenv("REMNAWAVE_TOKEN")

    # Initialize the SDK
    remnawave = RemnawaveSDK(base_url=base_url, token=token)

    # Fetch all users
    response: UsersResponseDto = await remnawave.users.get_all_users()
    total_users: int = response.total
    users: list[UserResponseDto] = response.users
    print("Total users: ", total_users)
    print("List of users: ", users)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## ❤️ About

This SDK was originally developed by [@kesevone](https://github.com/kesevone) for integration with Remnawave's API.

Previously maintained by [@sm1ky](https://github.com/sm1ky) at [`sm1ky/remnawave-api`](https://github.com/sm1ky/remnawave-api).

The official Remnawave repository is located at [`remnawave/python-sdk`](https://github.com/remnawave/python-sdk).

This repository is a fork of the official SDK.
