class Item:
    def __init__(self, name, category, price=0, **kwargs):
        self.name = name
        self.category = category # e.g. 'heal', 'ball', 'status', 'evolve'
        self.price = price
        # Additional fields depending on category
        self.heal_amount = kwargs.get('heal', 0)
        self.cure_status = kwargs.get('cure_status', None)
        self.catch_rate = kwargs.get('catch_rate', 1.0)
