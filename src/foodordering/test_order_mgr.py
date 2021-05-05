from order_mgr import getOrder

def test_single_item():
    order = getOrder("I want to order chicken briyani","")
    #print(order.toJSON())
    assert len(order.items) == 1
    for item in order.items :
        print(item.name)
        assert item.name == 'chicken briyani'
        assert item.quantity == 1

def test_two_items():
    order = getOrder("I want to order chicken briyani and chicken masala","")
    #print(order.toJSON())
    assert len(order.items) == 2
    assert order.items[0].name == 'chicken briyani'
    assert order.items[0].quantity == 1
    assert order.items[1].name == 'chicken masala'
    assert order.items[1].quantity == 1

def test_multiple_items_with_quantity1():
    order = getOrder("I want to order 1 chicken briyani, 2 chicken masala", "")
    #print(order.toJSON())
    assert len(order.items) == 2
    assert order.items[0].name == 'chicken briyani'
    assert order.items[0].quantity == 1
    assert order.items[1].name == 'chicken masala'
    assert order.items[1].quantity == 2

def test_multiple_items_with_quantity2():
    order = getOrder("I want to order two chicken briyani, 3 chicken masala and 12 garlic naan", "")
    #print(order.toJSON())
    assert len(order.items) == 3
    assert order.items[0].name == 'chicken briyani'
    assert order.items[0].quantity == 2
    assert order.items[1].name == 'chicken masala'
    assert order.items[1].quantity == 3
    assert order.items[2].name == 'garlic naan'
    assert order.items[2].quantity == 12


if __name__ == "__main__":
    test_single_item()
    test_two_items()
    test_multiple_items_with_quantity1()
    test_multiple_items_with_quantity2()
    print("Everything passed")