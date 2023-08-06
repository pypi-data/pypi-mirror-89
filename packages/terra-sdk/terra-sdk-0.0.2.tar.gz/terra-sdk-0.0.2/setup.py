# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terra_sdk',
 'terra_sdk.client',
 'terra_sdk.client.lcd',
 'terra_sdk.client.lcd.api',
 'terra_sdk.client.lcd.api.modules',
 'terra_sdk.client.lcd.api.modules.distribution',
 'terra_sdk.client.lcd.api.modules.gov',
 'terra_sdk.client.lcd.api.modules.market',
 'terra_sdk.client.lcd.api.modules.mint',
 'terra_sdk.client.lcd.api.modules.msgauth',
 'terra_sdk.client.lcd.api.modules.oracle',
 'terra_sdk.client.lcd.api.modules.slashing',
 'terra_sdk.client.lcd.api.modules.staking',
 'terra_sdk.client.lcd.api.modules.supply',
 'terra_sdk.client.lcd.api.modules.treasury',
 'terra_sdk.client.lcd.api.modules.tx',
 'terra_sdk.client.lcd.api.modules.wasm',
 'terra_sdk.core',
 'terra_sdk.core.auth',
 'terra_sdk.core.bank',
 'terra_sdk.core.bank.msgs',
 'terra_sdk.core.common',
 'terra_sdk.core.distribution',
 'terra_sdk.core.distribution.msgs',
 'terra_sdk.core.gov',
 'terra_sdk.core.gov.msgs',
 'terra_sdk.core.market',
 'terra_sdk.core.market.msgs',
 'terra_sdk.core.mint',
 'terra_sdk.core.msgauth',
 'terra_sdk.core.msgauth.msgs',
 'terra_sdk.core.oracle',
 'terra_sdk.core.oracle.msgs',
 'terra_sdk.core.slashing',
 'terra_sdk.core.slashing.msgs',
 'terra_sdk.core.staking',
 'terra_sdk.core.staking.msgs',
 'terra_sdk.core.treasury',
 'terra_sdk.core.wasm',
 'terra_sdk.core.wasm.msgs',
 'terra_sdk.key',
 'terra_sdk.utils']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=3.4.0,<4.0.0',
 'attrs>=20.3.0,<21.0.0',
 'bech32>=1.2.0,<2.0.0',
 'bip32utils>=0.3.post4,<0.4',
 'cached-property>=1.5.2,<2.0.0',
 'mnemonic>=0.19,<0.20',
 'requests-futures>=1.0.0,<2.0.0',
 'requests>=2.25.0,<3.0.0',
 'sphinx-rtd-theme>=0.5.0,<0.6.0',
 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'terra-sdk',
    'version': '0.0.2',
    'description': 'The Python SDK for Terra',
    'long_description': '# About\n    Terra python sdk\n\n# Installation\n    pip install terra_sdk\n\n# Usage\n    1. Creating, Signing, Broadcasting tx\n    2. Exposes the Terra API through LCDClient\n\n# Example\n* ## Transfer\n    ```python\n    from terra_sdk.core.common.coin import Coin\n    from terra_sdk.client import Terra, wallet\n    from terra_sdk.key.mnemonic import MnemonicKey\n    from terra_sdk.core.bank import MsgSend\n\n\n    LCD_URI = "http://localhost:1317"\n    CHAIN_ID = "localterra"\n    MNEMONIC = "satisfy adjust timber high purchase tuition stool faith fine install that you unaware feed domain license impose boss human eager hat rent enjoy dawn"\n\n    # Recover key from mnemonic\n    key = MnemonicKey(MNEMONIC)\n\n    # terra client\n    terra = Terra(chain_id=CHAIN_ID, lcd_url=LCD_URI)\n\n    # get user wallet\n    wallet = terra.wallet(key)\n\n    # Build Msg\n    send_msg = MsgSend(\n        from_address=wallet.address,\n        to_address="terra1dcegyrekltswvyy0xy69ydgxn9x8x32zdtapd8",\n        amount=[Coin(denom="uluna", amount="100000000")],\n    )\n\n    # Sign tx\n    signed_tx = wallet.create_and_sign_tx(send_msg, memo="Hi from Terra")\n\n    # Broadcast tx\n\n    resp = wallet.broadcast(signed_tx)\n\n    # Print txhash\n    print(resp.txhash)\n    ```',
    'author': 'Terraform Labs, PTE.',
    'author_email': 'engineering@terra.money',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/terra-project/terra-sdk-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
