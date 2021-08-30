import json

def update_order(n):
    '''Generate list of orders'''
    order = []
    for i in range(1, n+1):
        order.append([f'Order {i}', i])
    return order

# TODO: Make sure order.json is retrieved from the correct directory
with open('orders.json', 'w') as f:
    n = 5
    while True:
        order = update_order(n)
        json.dump(order, f)
        f.seek(0)
        if input('>>> Add new order? ').strip().lower()[0] == 'n':
            raise SystemExit
        n += 1