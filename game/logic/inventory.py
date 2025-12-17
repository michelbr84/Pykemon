import random
from game.data.items_data import items
from game.data.pokemon_data import species_data

def use_item(player, item_name, target=None, is_wild=False, battle=False, opponent=None):
    """
    Uses an item.
    Returns a dictionary:
    {
        'success': bool,
        'captured': bool, # specific for balls
        'messages': list[str]
    }
    """
    result = {
        'success': False,
        'captured': False,
        'messages': []
    }
    
    if item_name not in player.inventory or player.inventory[item_name] <= 0:
        result['messages'].append("You don't have that item.")
        return result
    
    item = items.get(item_name)
    if not item:
        result['messages'].append("Unknown item.")
        return result

    # Poké Ball usage
    if item.category == "ball":
        if not battle:
            result['messages'].append("You can't use that here.")
            return result
        if not is_wild:
            result['messages'].append("You can't use that on someone else's Pokemon!")
            return result
        
        # Auto-target opponent if not specified
        if target is None and opponent:
            target = opponent
            
        if target is None or target.current_hp <= 0:
             result['messages'].append("There's no valid target for the ball.")
             return result

        # Use the Poké Ball
        player.inventory[item_name] -= 1
        if player.inventory[item_name] == 0:
            del player.inventory[item_name]
            
        # Catch chance calculation
        health_ratio = target.current_hp / target.max_hp
        catch_chance = (0.8 * (1 - health_ratio) + 0.1) * item.catch_rate
        if catch_chance > 0.95: catch_chance = 0.95
        if catch_chance < 0.05: catch_chance = 0.05
        
        if random.random() < catch_chance:
            result['messages'].append(f"Gotcha! {target.species} was caught!")
            player.add_pokemon(target)
            result['success'] = True
            result['captured'] = True
            return result
        else:
            result['messages'].append(f"The wild {target.species} broke free!")
            result['success'] = True
            return result

    elif item.category == "heal":
        if target is None:
            result['messages'].append("No target specified.")
            return result
        if target.current_hp <= 0:
            result['messages'].append(f"{target.species} is fainted and can't be healed!")
            return result
            
        original_hp = target.current_hp
        target.current_hp += item.heal_amount
        if target.current_hp > target.max_hp:
            target.current_hp = target.max_hp
        healed = target.current_hp - original_hp
        
        result['messages'].append(f"{target.species} regained {healed} HP.")
        player.inventory[item_name] -= 1
        if player.inventory[item_name] == 0:
            del player.inventory[item_name]
        result['success'] = True
        return result

    elif item.category == "status":
        if target is None:
            result['messages'].append("No target specified.")
            return result
        if target.status is None:
            result['messages'].append(f"{target.species} has no status condition.")
            return result
        
        if item.cure_status and target.status == item.cure_status:
            target.status = None
            result['messages'].append(f"{target.species} was cured of its {item.cure_status} condition!")
        else:
            result['messages'].append("It had no effect.")
            player.inventory[item_name] -= 1
            if player.inventory[item_name] == 0:
                del player.inventory[item_name]
            return result 
            
        player.inventory[item_name] -= 1
        if player.inventory[item_name] == 0:
            del player.inventory[item_name]
        result['success'] = True
        return result

    elif item.category == "evolve":
        if battle:
            result['messages'].append("You can't use that in the middle of a battle!")
            return result
        if target is None:
            result['messages'].append("No target specified for evolution.")
            return result
            
        if "evolve_item" in species_data[target.species] and species_data[target.species]["evolve_item"] == item_name:
            new_species = species_data[target.species]["evolves_to"]
            msgs = target.evolve(new_species)
            result['messages'].extend(msgs)
            # Update Pokédex
            player.pokedex_seen.add(new_species)
            player.pokedex_caught.add(new_species)
        else:
            result['messages'].append("It had no effect.")
            player.inventory[item_name] -= 1
            if player.inventory[item_name] == 0:
                del player.inventory[item_name]
            return result 

        player.inventory[item_name] -= 1
        if player.inventory[item_name] == 0:
            del player.inventory[item_name]
        result['success'] = True
        return result

    else:
        result['messages'].append("This item cannot be used now.")
        return result
