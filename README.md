# Greek Scrabble (Python)

## Overview
This is a Scrabble-like word game implemented in **Python**.  
The interface (menus, messages) is in **English** for accessibility, but the game logic, dictionary, and scoring are based on **Greek words and letters**.  

Players can compete against the computer, which supports multiple AI strategies.

---

## Features
- Bag of Greek Scrabble letters with correct distribution and scores.  
- Human vs Computer gameplay.  
- Computer strategies:
  - **MIN** → plays shortest words first  
  - **MAX** → plays longest words first  
  - **SMART** → plays the highest scoring word  
  - **FAIL** → sometimes plays a weaker word  
  - **LEARN** → learns new words from the human  
  - **TEACH** → suggests the best possible word  

---

## How to Run
1. Clone or download this repository.  
2. Make sure you have Python 3 installed.  
3. Run the game:  
   ```bash
   python main.py

