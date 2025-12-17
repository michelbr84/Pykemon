from game.data.items_data import items

class ShopLogic:
    MART_ITEMS = [("Pokeball", 100), ("Potion", 100), ("Super Potion", 300), ("Thunder Stone", 1000)]

    @staticmethod
    def get_items_for_sale():
        """Returns list of (name, price) tuples"""
        return ShopLogic.MART_ITEMS

    @staticmethod
    def buy_item(player, item_idx_1_based, quantity):
        """
        Returns { "success": bool, "message": str }
        """
        if item_idx_1_based < 1 or item_idx_1_based > len(ShopLogic.MART_ITEMS):
            return {"success": False, "message": "Invalid item selection."}
            
        item_name, price = ShopLogic.MART_ITEMS[item_idx_1_based - 1]
        
        if quantity <= 0:
            return {"success": False, "message": "Invalid quantity."}
            
        cost = price * quantity
        if player.money < cost:
            return {"success": False, "message": "You don't have enough money."}
            
        player.money -= cost
        player.inventory[item_name] = player.inventory.get(item_name, 0) + quantity
        return {"success": True, "message": f"You bought {quantity} {item_name}(s) for ${cost}."}

    @staticmethod
    def get_sellable_items(player):
        """Returns list of (item_name, qty, sell_price)"""
        sellable = []
        for name, qty in player.inventory.items():
            if name in items:
                price = items[name].price // 2
                sellable.append((name, qty, price))
        return sellable

    @staticmethod
    def sell_item(player, item_name, quantity):
        """
        Returns { "success": bool, "message": str }
        """
        if item_name not in player.inventory:
            return {"success": False, "message": "You don't have that item."}
            
        if quantity <= 0 or quantity > player.inventory[item_name]:
            return {"success": False, "message": "Invalid quantity."}
            
        item_data = items.get(item_name)
        sell_price = item_data.price // 2 if item_data else 0
        
        total_gain = sell_price * quantity
        player.inventory[item_name] -= quantity
        if player.inventory[item_name] == 0:
            del player.inventory[item_name]
            
        player.money += total_gain
        return {"success": True, "message": f"You sold {quantity} {item_name}(s) for ${total_gain}."}
