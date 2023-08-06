# About
    Terra python sdk

# Installation
    pip install terra_sdk

# Usage
    1. Creating, Signing, Broadcasting tx
    2. Exposes the Terra API through LCDClient

# Example
* ## Transfer
    ```python
    from terra_sdk.core.common.coin import Coin
    from terra_sdk.client import Terra, wallet
    from terra_sdk.key.mnemonic import MnemonicKey
    from terra_sdk.core.bank import MsgSend


    LCD_URI = "http://localhost:1317"
    CHAIN_ID = "localterra"
    MNEMONIC = "satisfy adjust timber high purchase tuition stool faith fine install that you unaware feed domain license impose boss human eager hat rent enjoy dawn"

    # Recover key from mnemonic
    key = MnemonicKey(MNEMONIC)

    # terra client
    terra = Terra(chain_id=CHAIN_ID, lcd_url=LCD_URI)

    # get user wallet
    wallet = terra.wallet(key)

    # Build Msg
    send_msg = MsgSend(
        from_address=wallet.address,
        to_address="terra1dcegyrekltswvyy0xy69ydgxn9x8x32zdtapd8",
        amount=[Coin(denom="uluna", amount="100000000")],
    )

    # Sign tx
    signed_tx = wallet.create_and_sign_tx(send_msg, memo="Hi from Terra")

    # Broadcast tx

    resp = wallet.broadcast(signed_tx)

    # Print txhash
    print(resp.txhash)
    ```