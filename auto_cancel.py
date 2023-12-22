from be.model.buyer import Buyer
def delete_order_time():
    buyer = Buyer()
    while True:
        buyer.delete_order_time()
if __name__ == '__main__':
    delete_order_time()