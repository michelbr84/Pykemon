# Official Pykemon Game Guide

## 1. Introduction

Welcome to **Pykemon**! This guide is designed to help you navigate, battle, and progress through the game. Whether you are a new player or returning, this document outlines everything you need to know to become a Pokémon Master.

This guide explains your objectives, how to overcome obstacles (such as Team Rocket and Gyms), and how to use the game's controls effectively.

---

## 2. How to Start the Game

Upon launching the game (`run_game_gui.py`), you will see the Title Screen.

*   **New Game**: Starts a fresh adventure. You begin in **Pallet Town** with a Level 5 starter Pokémon, **Pyron**.
*   **Load Game**: Loads your previously saved progress (from `Ash.json`).
*   **Quit**: Exits the application.

### Controls

*   **Mouse**: Navigate the Main Menu by hovering and clicking options.
*   **Arrow Keys**: Move your character on the Map.
*   **Interaction Shortcuts (Map Only)**:
    *   **[G]**: Challenge the Gym Leader (Only in Viridian City).
    *   **[H]**: Heal your Party (Only in Towns/Cities).
    *   **[S]**: Save your Game.

---

## 3. Core Gameplay Loop

1.  **Exploration**: Use the **Arrow Keys** to move between locations. Walk into the edges of the screen to travel to adjacent areas (e.g., North from Pallet Town leads to Route 1).
2.  **Wild Encounters**: While walking in Routes (e.g., Route 1, Route 2), you have a chance to encounter wild Pokémon. Defeat them to gain Experience (XP).
3.  **Leveling Up**: Gaining XP allows your Pokémon to level up, increasing stats (HP, Attack, Defense, Speed) and learning new moves automatically.
4.  **Evolution**: Some Pokémon evolve upon reaching specific levels (e.g., Pyron evolves at Level 10).

---

## 4. Progression Path (CRITICAL)

To beat the current version of the game, follow this exact path:

1.  **Start in Pallet Town**: Familiarize yourself with controls.
2.  **Go North to Route 1**: defeat **Youngster Joey** (mandatory battle) to proceed.
3.  **Arrive in Viridian City**:
    *   **Heal**: Press **[H]** to heal your team.
    *   **Save**: Press **[S]** to save your progress.
    *   **Blocked Path**: If you try to go North to Route 2, a Policeman will stop you. He says: *"The road ahead is closed due to Team Rocket. You need a Gym Badge to pass!"*
4.  **Obtain the Boulder Badge**:
    *   Stay in **Viridian City**.
    *   Press **[G]** to challenge **Gym Leader Rocky**.
    *   **Win the battle** to obtain the **Boulder Badge**.
5.  **Proceed to Route 2**: With the badge, the Policeman will let you pass. A Rival Battle may trigger here!
6.  **Reach Rocket Hideout**: Go North from Route 2. Defeat the Grunt and the Boss to complete the current story.

---

## 5. Gyms & Badges

Gyms are challenging battles that unlock new areas.

### Viridian City Gym
*   **Leader**: Rocky
*   **Team**: Geon (Lv 8), Geodon (Lv 12)
*   **Type**: Rock (Weak to Water and Grass; Resistant to Fire)
*   **How to Enter**: Press **[G]** while in Viridian City.
*   **Reward**: **Boulder Badge**. Unlocks access to Route 2.

---

## 6. NPCs & Interactions

*   **Youngster Joey** (Route 1): Blocks the path until defeated.
*   **Policeman** (Viridian City Exit): Blocks access to Route 2 until you have the **Boulder Badge**.
*   **Rival**: Appears periodically to test your strength.
*   **Team Rocket**: The antagonists found in the Hideout. Defeating the Boss is the final objective.

---

## 7. Battle Controls & Menus

When a battle starts, you will see your Pokémon (bottom left) and the opponent (top right).

### Battle Menu Shortcuts
Press the corresponding number key to select an action:
1.  **FIGHT**: Opens the Move Selection menu.
2.  **BAG**: *Not fully implemented in this version.*
3.  **POKEMON**: *Not fully implemented in this version.*
4.  **RUN**: Attempt to flee (Only works in Wild Battles).

### Move Selection
After pressing **[1] (FIGHT)**, press **1-4** to use a move:
*   **[1]**: Move 1 (e.g., Tackle)
*   **[2]**: Move 2 (e.g., Ember - Unlocks at Lv 5)
*   **[3]**: Move 3
*   **[4]**: Move 4

---

## 8. Items & Inventory

*   **Potion**: Heals 20 HP.
*   **Super Potion**: Heals 50 HP.
*   **Antidote**: Cures Poison.
*   **Paralyze Heal**: Cures Paralysis.
*   **Poké Ball**: Used to catch wild Pokémon (Only usable in Wild Battles).

*Note: In the current GUI version, item usage is automatic via events or strictly controlled scenarios. Full inventory menu access is coming in a future update.*

---

## 9. Saving & Loading

*   **Save**: Press **[S]** at any time on the Map to save your progress to `Ash.json`.
*   **Autosave**: The game does **not** autosave. You must save manually before quitting.
*   **Load**: Select "Load Game" from the Title Screen to resume your adventure.

Good luck, Trainer!
