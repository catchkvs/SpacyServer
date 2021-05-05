from google.cloud import firestore
import copy

def saveOrder(order) :
    orderCopy = copy.deepcopy(order)
    db = firestore.Client()
    new_order_ref = db.collection("orders").document()
    order_items = []
    for item in orderCopy.items:
        order_items.append(item.to_dict())
    orderCopy.items = order_items
    new_order_ref.set(orderCopy.to_dict())
    return new_order_ref.id 


def main() :
    #saveOrder(getOrder("i want to order chiken briyani", ""))
    print("saveOrder")

if __name__ == "__main__":
    main()