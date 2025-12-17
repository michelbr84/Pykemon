from game.models.items import Item

# Predefined available item data (used for Mart pricing and effects)
items = {
    "Pokeball": Item("Pokeball", "ball", price=100, catch_rate=1.0),
    "Potion": Item("Potion", "heal", price=100, heal=20),
    "Super Potion": Item("Super Potion", "heal", price=300, heal=50),
    "Antidote": Item("Antidote", "status", price=50, cure_status="poisoned"),
    "Paralyze Heal": Item("Paralyze Heal", "status", price=50, cure_status="paralyzed"),
    "Thunder Stone": Item("Thunder Stone", "evolve", price=1000)
}
