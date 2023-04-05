import logging
from binance.pay.merchant import Merchant as Client
from binance.pay.lib.utils import config_logging




key = "qB2CzYEwUt56FYY0rhchejUEs6F0WacSvMfdmmFOoJBEsUsM06QqAJipDuZM2ZSZ"
secret = "qyeRSnnnDqI6bIUCVYnsu2Ai7V5n3FIaHmmCp7Ft9vQ0mEs3PEntkyIDbQB9CUS3"

client = Client(key, secret)
config_logging(logging, logging.DEBUG)


response = client.get_transfer_result("2346")