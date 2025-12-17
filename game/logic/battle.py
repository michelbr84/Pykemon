import random
from game.data.moves_data import moves
from game.data.pokemon_data import type_effectiveness
from game.logic.inventory import use_item

class Battle:
    def __init__(self, player, opponent, is_wild=False, link_battle=False):
        self.player = player
        self.opponent = opponent
        self.is_wild = is_wild
        self.link_battle = link_battle
        self.logs = []
        self.finished = False
        self.won = False
        
        # Initialize active Pokemon
        self.active_player_mon = self._get_first_alive(player.pokemon)
        
        if is_wild:
            self.active_opponent_mon = opponent # In wild battle, opponent is the Pokemon object
            self.opponent_name = "Wild"
        else:
            self.active_opponent_mon = self._get_first_alive(opponent.pokemon)
            self.opponent_name = opponent.name
            
            # Heal opponent for fairness (as per original logic)
            if not link_battle: # Original logic healed regardless? "Heal opponent's Pokémon at battle start"
                 # checking original code line 420: yes healed.
                 for mon in opponent.pokemon:
                     if mon.current_hp <= 0:
                         mon.current_hp = mon.max_hp
                         mon.status = None
            
        # Initial logs
        if is_wild:
            self.logs.append(f"A wild {self.active_opponent_mon.species} appeared!")
        else:
            self.logs.append(f"{self.opponent_name} wants to battle!")
            self.logs.append(f"{self.opponent_name} sent out {self.active_opponent_mon.species}!")
        self.logs.append(f"Go! {self.active_player_mon.species}!")
        
        # Pokedex
        player.pokedex_seen.add(self.active_opponent_mon.species)

    def _get_first_alive(self, party):
        for mon in party:
            if mon.current_hp > 0:
                return mon
        return None

    def execute_turn(self, action):
        """
        action: tuple
          ("fight", move_name)
          ("item", item_name, target_idx?) 
             -> Refactored: ("item", item_name, target_obj)
          ("switch", new_mon_obj)
          ("run",)
        
        Returns: { 'ended': bool, 'logs': list[str] }
        """
        self.logs = [] # clear logs for this turn
        player_mon = self.active_player_mon
        opp_mon = self.active_opponent_mon
        
        # 1. Handle Run
        if action[0] == "run":
            if not self.is_wild:
                 self.logs.append("You can't run from a trainer battle!")
                 # Logic continues to opponent attack? Original: yes "run failed" (action='run_failed')
                 # But standard pokemon logic: Trainer battle -> fail run -> opponent attacks?
                 # Main.py Lines 567-568: "continue" (re-prompt).
                 # To support that, we need to return "invalid" or handle it.
                 # Simpler: Main loop handles "Can't run". If we are here, we attempt run?
                 # Assume UI blocked it if trainer battle. But if it got here:
                 pass 
            else:
                run_chance = 1.0
                if opp_mon.speed > player_mon.speed:
                    run_chance = 0.5
                
                if random.random() < run_chance:
                    self.logs.append("Got away safely!")
                    self.finished = True
                    return {'ended': True, 'logs': self.logs}
                else:
                    self.logs.append("Couldn't escape!")
                    # Continues to opponent turn ("run_failed")

        # 2. Handle Switch
        if action[0] == "switch":
            new_mon = action[1]
            self.logs.append(f"Come back, {player_mon.species}!")
            self.logs.append(f"Go, {new_mon.species}!")
            self.active_player_mon = new_mon
            player_mon = new_mon # Update reference
            # Opponent gets free hit

        # 3. Handle Item
        caught_pokemon = False
        if action[0] == "item":
            item_name = action[1]
            target = action[2] if len(action) > 2 else None
            
            # Special case: Ball needs opponent as implicit target (fixed logic)
            # Logic handled in use_item now
            
            # is_wild check passed to use_item
            res = use_item(self.player, item_name, target=target, is_wild=self.is_wild, battle=True, opponent=opp_mon)
            self.logs.extend(res['messages'])
            
            if res.get('captured'):
                self.finished = True
                self.won = True 
                return {'ended': True, 'logs': self.logs}
            
            if not res['success']:
                # If item failed, does turn end? Main.py continues loop if use_item returns True (ends battle)
                # If use_item returns False, it continues to opponent attack?
                # Main.py: "action = ('item_used', ...)" -> Executes opponent turn.
                pass

        # 4. Determine Opponent Move
        opp_move_name = None
        if opp_mon.moves:
            opp_move_name = random.choice(opp_mon.moves)
        
        # 5. Execute Moves (if action is fight)
        if action[0] == "fight":
            player_move_name = action[1]
            player_first = True
            if opp_mon.speed > player_mon.speed:
                player_first = False
            
            first = (self.player, player_mon, player_move_name) if player_first else (self.opponent, opp_mon, opp_move_name)
            second = (self.opponent, opp_mon, opp_move_name) if player_first else (self.player, player_mon, player_move_name)
            
            # Execute First
            self._execute_move(first[1], second[1], first[2], is_player=(first[0] == self.player))
            
            # Check Faint after first
            if second[1].current_hp <= 0:
                self._handle_faint(second[1], is_player=(second[0] == self.player))
                if self.finished: return {'ended': True, 'logs': self.logs}
            else:
                # Execute Second
                self._execute_move(second[1], first[1], second[2], is_player=(second[0] == self.player))
                # Check Faint after second
                if first[1].current_hp <= 0:
                     self._handle_faint(first[1], is_player=(first[0] == self.player))
                     if self.finished: return {'ended': True, 'logs': self.logs}

        # 6. Execute Opponent Move (if action was item/switch/run_fail)
        elif action[0] in ["item", "switch", "run", "run_failed"]:
            if opp_mon.current_hp > 0:
                 self._execute_move(opp_mon, player_mon, opp_move_name, is_player=False)
                 if player_mon.current_hp <= 0:
                     self._handle_faint(player_mon, is_player=True)
                     if self.finished: return {'ended': True, 'logs': self.logs}

        # 7. Status Effects (End of turn)
        self._handle_status(player_mon)
        if player_mon.current_hp <= 0: # Check faint from poison
             self._handle_faint(player_mon, is_player=True)
             if self.finished: return {'ended': True, 'logs': self.logs}
             
        self._handle_status(opp_mon)
        if opp_mon.current_hp <= 0:
             self._handle_faint(opp_mon, is_player=False)
             if self.finished: return {'ended': True, 'logs': self.logs}

        return {'ended': False, 'logs': self.logs}

    def _execute_move(self, attacker, defender, move_name, is_player):
        if not move_name: return
        
        # Check Paralysis
        if attacker.status == "paralyzed":
            if random.random() < 0.25:
                self.logs.append(f"{attacker.species} is paralyzed and can't move!")
                return

        move = moves[move_name]
        self.logs.append(f"{attacker.species} used {move_name}!")
        
        if random.random() > move.accuracy:
            self.logs.append("But it missed!")
            return
            
        damage = int(move.power * attacker.attack / max(1, defender.defense) / 2)
        if damage < 1: damage = 1
        
        # Type effectiveness
        eff_mult = 1.0
        if move.type:
            key = (move.type, defender.type)
            if key in type_effectiveness:
                eff_mult = type_effectiveness[key]
        
        damage = int(damage * eff_mult * random.uniform(0.85, 1.0))
        if damage < 1: damage = 1
        
        defender.current_hp -= damage
        self.logs.append(f"It did {damage} damage.")
        
        if eff_mult > 1: self.logs.append("It's super effective!")
        elif 0 < eff_mult < 1: self.logs.append("It's not very effective...")
        
        # Move Effects
        if move.effect and defender.current_hp > 0:
            if defender.status is None and random.random() < move.effect_chance:
                # Grammar adjustment
                status = move.effect + "ed" if move.effect != "paralyze" else "paralyzed"
                defender.status = status
                self.logs.append(f"{defender.species} was {status}!")

    def _handle_faint(self, mon, is_player):
        mon.current_hp = 0
        mon.status = None # Reset status on faint
        if is_player:
            self.logs.append(f"Your {mon.species} fainted!")
            pass # TODO: Logic for forced switch?
            # In this engine, we check if any alive.
            if not any(p.current_hp > 0 for p in self.player.pokemon):
                self.logs.append("You have no more Pokemon!")
                self.finished = True
                self.won = False
            else:
                pass # Game/UI needs to prompt switch. 
                # Ideally, we return specific state "WAITING_FOR_SWITCH".
        else:
            self.logs.append(f"{mon.species} fainted!")
            # XP Gain
            if not self.link_battle:
                exp = mon.level * 20
                res = self.active_player_mon.gain_exp(exp)
                self.logs.append(f"Gained {exp} XP.")
                self.logs.extend(res['messages'])
                # "gain_exp" logic changed in new model.
            
            if self.is_wild:
                self.finished = True
                self.won = True
                return
            
            # Trainer battle: check next mon
            next_mon = self._get_first_alive(self.opponent.pokemon)
            if next_mon:
                self.active_opponent_mon = next_mon
                self.logs.append(f"{self.opponent_name} sent out {next_mon.species}!")
                self.player.pokedex_seen.add(next_mon.species)
            else:
                self.finished = True
                self.won = True
                self.logs.append("You won the battle!")

    def _handle_status(self, mon):
        if mon.status == "poisoned":
            dmg = max(1, mon.max_hp // 10)
            mon.current_hp -= dmg
            self.logs.append(f"{mon.species} is hurt by poison!")
        elif mon.status == "burned":
            dmg = max(1, mon.max_hp // 10)
            mon.current_hp -= dmg
            self.logs.append(f"{mon.species} is hurt by its burn!")
