# BCHydro API

![PyPi publish](https://github.com/emcniece/bchydro/workflows/Publish%20PyPi/badge.svg) ![PyPi version](https://img.shields.io/pypi/v/bchydro)

BCHydro Python API for extracting electricity usage statistics from your personal account.

## Installation

Via [PyPi](https://pypi.org/project/bchydro/):

```sh
pip install bchydro
```

Via Github:

```sh
git clone https://github.com/emcniece/bchydro.git
cd bchydro
pip install -r requirements.txt
```

## Usage

Running the example script:

```sh
pip install bchydro

export BCH_USER=your.email@domain.com
export BCH_PASS=your-bch-password

python test.py
```

Using in a project:

```py
import asyncio
from bchydro import BCHydroApi

async def main():
    a = BCHydroApi()
    await a.authenticate("username", "password")

    usage = await a.get_usage(hourly=False)
    print(usage.electricity)
    print(a.get_latest_point())
    print(a.get_latest_usage())
    print(a.get_latest_cost())

asyncio.run(main())
```

BCHydro offers [view-only accounts](https://app.bchydro.com/BCHCustomerPortal/web/accountAccessView.html),
as a more secure option.


## Version Publishing

This repo is automatically published to [PyPi](https://pypi.org/project/bchydro/) by means of a [Github Workflow](https://github.com/emcniece/bchydro/actions?query=workflow%3A%22Publish+PyPi%22) when a new [release](https://github.com/emcniece/bchydro/releases) is created on Github.


## Todo

- [x] Publish on release, not tag
- [x] Handle account locking (looks for HTML alert dialogs)
- [ ] Unit tests


## Disclaimer

This package has been developed without the express permission of BC Hydro. It accesses data by submitting forms that end-users would typically use in a browser. I'd love to work with BC Hydro to find a better way to access this data, perhaps through an official API... if you know anyone that works there, pass this along!
