from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled',
              filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange,
              ':', order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency,
              execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        super().position(account, contract, position, avgCost)
        print("Position.", "Account:", account, "Symbol:", contract.symbol, "SecType:",
        contract.secType, "Currency:", contract.currency, "Position:", position, "Avg cost:", avgCost)




# Function to create FX Order contract


def FX_order(symbol):
    contract = Contract()
    contract.symbol = symbol[:3]
    contract.secType = 'CASH'
    contract.exchange = 'IDEALPRO'
    contract.currency = symbol[3:]
    return contract

def createInstance(address,port,client_ID):
    app = IBapi()
    app.connect(address,port,client_ID)
    app.nextorderId = None
    return app

master_app = createInstance('127.0.0.1', 7496, 1)


apps = [] 


start_port = 7498
start_client = 124
for i in range(2):
    temp_app = createInstance('127.0.0.1', start_port + i, start_client + i)
    apps.append(temp_app)


def run_loop():
    for app in apps:
        app.run()
        while not isinstance(app.nextorderId, int):
            print('connecting')
            app.run()
        print('connected')
    
    # will only come out of the instance if it is a instance. thus connect after break
    #     
    # app.run()
    # app2.run()


# app = IBapi()
# app2 = IBapi()
# app.connect('127.0.0.1', 7496, 124)
# app2.connect('127.0.0.1', 7498, 125)
# send data to another port
# 
# app.nextorderId = None
# app2.nextorderId = None

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

# Check if the API is connected via orderid
# while True:
#     if isinstance(app.nextorderId, int):
#         print('connected')
#         break
#     else:
#         print('waiting for connection')
#         time.sleep(1)

# Create order object
order = Order()
order.action = 'BUY'
order.totalQuantity = 100000
order.orderType = 'LMT'
order.lmtPrice = '1.10'

# Place order
# app.placeOrder(app.nextorderId, FX_order('EURUSD'), order)
# app2.placeOrder(app.nextorderId, FX_order('EURUSD'), order)
#app.nextorderId += 1

# app.reqPositions()

# time.sleep(3)

# Cancel order
# print('cancelling order')
# app.cancelOrder(app.nextorderId)

# time.sleep(3)
# app.disconnect()
