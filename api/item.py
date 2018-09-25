class Item():
    def __init__(self):
        self.item_list = [
            {
                'name': 'Chips + Chicken',
                'quantity_available': 0
            },
            {
                'name': 'Pizza',
                'quantity_available': 0
            },
            {
                'name': 'Cheese Burger',
                'quantity_available': 0
            },
            {
                'name': 'Plain Chips',
                'quantity_available': 0
            },
            {
                'name': 'Fried Eggs',
                'quantity_available': 0
            },
            {
                'name': 'Sandwich',
                'quantity_available': 0
            }
        ]

    def getItemQuantity(self, name):
        for quantity in self.item_list:
            if quantity['name'] == name:
                return quantity['quantity_available']

    def setItemQuantity(self, name, quantity):
        for item in self.item_list:
            if item['name'] == name:
                item['quantity_available'] = quantity
