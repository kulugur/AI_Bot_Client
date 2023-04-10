import logging
from binance.pay import
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from examples.utils.prepare_env import get_api_key

config_logging(logging, logging.DEBUG)

key = "Egl6wWqGhkRk4sRgkdSQPHFzD23x7Avk62ymeZgSoDLx2ggaOwdBpVqkArX05NDn"
secret = "4ugWERvG56ZB2vpA5uINhEkFEG56FeE7cckf9FsmHS1AntrMhiipXnJurzAkfpRa"

spot_client = Client(key, secret)
infio = spot_client.deposit_address(coin="USDT")
logging.info(spot_client.deposit_address(coin="USDT"))


#
#
# key = "qB2CzYEwUt56FYY0rhchejUEs6F0WacSvMfdmmFOoJBEsUsM06QqAJipDuZM2ZSZ"
# secret = "qyeRSnnnDqI6bIUCVYnsu2Ai7V5n3FIaHmmCp7Ft9vQ0mEs3PEntkyIDbQB9CUS3"
#
# client = Client(key, secret)
# config_logging(logging, logging.DEBUG)
#
#
# response = client.get_transfer_result("2346")