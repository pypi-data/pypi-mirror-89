import base64
import hashlib
import json
import requests
from typing import Any, Dict, List

import ecdsa

from cyberpy._wallet import privkey_to_address, privkey_to_pubkey
from cyberpy.typing import SyncMode


class Transaction:
    """A Cyber transaction.

    After initialization, one or more token transfers can be added by
    calling the `add_transfer()`, `add_cyberlink` method. Then, call `get_pushable()`
    to get a signed transaction that can be pushed to the `POST /txs`
    endpoint of the Cyber REST API or call `broadcast(LCD_API=<LCD_API>)` method
    to get signed transaction and broadcast it with LCD_API.
    """

    def __init__(
        self,
        *,
        privkey: bytes,
        account_num: int,
        sequence: int,
        fee: int,
        gas: int,
        fee_denom: str = "eul",
        memo: str = "test",
        chain_id: str = "euler-6",
        sync_mode: SyncMode = "sync",
    ) -> None:
        self._privkey = privkey
        self._account_num = account_num
        self._sequence = sequence
        self._fee = fee
        self._fee_denom = fee_denom
        self._gas = gas
        self._memo = memo
        self._chain_id = chain_id
        self._sync_mode = sync_mode
        self._msgs: List[dict] = []

    def add_transfer(self, recipient: str, amount: int, denom: str = "eul") -> None:
        transfer = {
            "type": "cosmos-sdk/MsgSend",
            "value": {
                "from_address": privkey_to_address(self._privkey),
                "to_address": recipient,
                "amount": [{"denom": denom, "amount": str(amount)}]
            }
        }
        self._msgs.append(transfer)

    def add_cyberlink(self, cid_from: str, cid_to: str) -> None:
        cyberlink = {
            "type": "cyber/Link",
            "value": {
                "address": privkey_to_address(self._privkey),
                "links": [{"from": cid_from, "to": cid_to}]
            }
        }
        self._msgs.append(cyberlink)

    def add_delegation(self, validator: str, amount: int, denom: str = "eul") -> None:
        delegation = {
            "type": "cosmos-sdk/MsgDelegate",
            "value": {
                "delegator_address": privkey_to_address(self._privkey),
                "validator_address": validator,
                "amount": {"denom": denom, "amount": str(amount)}
            }
        }
        self._msgs.append(delegation)

    def add_undelegation(self, validator:  str, amount: int, denom: str = "eul"):
        undelegation = {
            "type": "cosmos-sdk/MsgUndelegate",
            "value": {
                "delegator_address": privkey_to_address(self._privkey),
                "validator_address": validator,
                "amount": {"denom": denom, "amount": str(amount)}
            }
        }
        self._msgs.append(undelegation)

    def add_redelegation(self, validator_src: str, validator_dst: str, amount: int, denom: str = "eul"):
        redelegation = {
            "type": "cosmos-sdk/MsgBeginRedelegate",
            "value": {
                "delegator_address": privkey_to_address(self._privkey),
                "validator_src_address": validator_src,
                "validator_dst_address": validator_dst,
                "amount": {"denom": denom, "amount": str(amount)}
            }
        }
        self._msgs.append(redelegation)

    def add_withdraw(self, validator: str):
        withdraw = {
            "type": "cosmos-sdk/MsgWithdrawDelegationReward",
            "value": {
                "delegator_address": privkey_to_address(self._privkey),
                "validator_address": validator
            }
        }
        self._msgs.append(withdraw)


    def get_pushable(self) -> str:
        pubkey = privkey_to_pubkey(self._privkey)
        base64_pubkey = base64.b64encode(pubkey).decode("utf-8")
        pushable_tx = {
            "tx": {
                "msg": self._msgs,
                "fee": {
                    "gas": "200000",
                    "amount": [],
                },
                "memo": self._memo,
                "signatures": [
                    {
                        "signature": self._sign(),
                        "pub_key": {"type": "tendermint/PubKeySecp256k1", "value": base64_pubkey},
                        "account_number": str(self._account_num),
                        "sequence": str(self._sequence),
                    }
                ],
            },
            "mode": self._sync_mode,
        }
        return json.dumps(pushable_tx, separators=(",", ":"))

    def broadcast(self, LCD_API: str):
        res = requests.post(url=LCD_API + '/txs', data=self.get_pushable())
        if res.status_code == 200:
            res = res.json()
            return res
        else:
            raise Exception("Broadcact failed to run by returning code of {}".format(res.status_code))


    def _sign(self) -> str:
        message_str = json.dumps(self._get_sign_message(), separators=(",", ":"), sort_keys=True)
        message_bytes = message_str.encode("utf-8")

        privkey = ecdsa.SigningKey.from_string(self._privkey, curve=ecdsa.SECP256k1)
        signature_compact = privkey.sign_deterministic(
            message_bytes, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_string_canonize
        )

        signature_base64_str = base64.b64encode(signature_compact).decode("utf-8")
        return signature_base64_str

    def _get_sign_message(self) -> Dict[str, Any]:
        return {
            "chain_id": self._chain_id,
            "account_number": str(self._account_num),
            "fee": {
                "gas": "200000",
                "amount": [],
            },
            "memo": self._memo,
            "sequence": str(self._sequence),
            "msgs": self._msgs,
        }