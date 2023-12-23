from be.model.buyer import Buyer
from be.model.store import init_database
def delete_order_time():
    init_database()
    buyer = Buyer()
    while True:
        buyer.delete_order_time()
if __name__ == '__main__':
    delete_order_time()