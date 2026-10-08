#  Pixel Quest

> A fun and interactive image puzzle game built with Python and Tkinter, where players rearrange shuffled image pieces to complete the original picture.

---

##  About the Project

Pixel Quest challenges players to recognize objects hidden behind a grid of covered squares.

As you progress through the game, the puzzles become more difficult with larger grids. Players must balance how much of the image they reveal with how quickly they can make the correct guess.

The game currently features two themed worlds:

🍎 Fruit World

🥦 Vegetable World

Each world contains three progressively challenging levels.
---

##  Features

###  Progressive Puzzle Difficulty

Each level uses a different grid size:

| Level | Grid |
|---|---:|
| Level 1 | 3 × 3 |
| Level 2 | 4 × 4 |
| Level 3 | 5 × 5 |

The increasing grid size makes later challenges more difficult.

###  30-Second Countdown

Every level starts with a **30-second timer**.

The timer changes appearance during the final five seconds and produces a warning sound as time runs out.

###  Reveal & Guess Gameplay

Players must reveal at least one square before submitting an answer.

If the guess is incorrect, another square can be revealed before trying again.

This creates a simple strategic challenge:

> **Reveal more → gain more information, but risk losing time and points.**

###  Scoring System

Correct guesses award points based on the number of attempts.

```text
Points = max(10, 110 - (Attempt × 10))
```

Fewer attempts mean a higher score.

###  High Score System

Pixel Quest automatically saves the player's best score to:

```text
highscore.txt
```

The saved record is loaded when the game starts, allowing players to compete against their previous best score.

###  Sound Effects

The game uses Windows system sounds for:

-  Correct answers
-  Wrong answers
-  Countdown warnings

###  Interactive GUI

The interface includes:

- World introduction screens
- Image-based puzzles
- Interactive reveal grids
- Answer choices
- Score tracking
- High-score tracking
- Countdown timer
- Game-over screens
- Victory screens

##  Worlds & Levels

### 🍎 Fruit World

| Level | Grid | Answer |
|---|---:|---|
| 1 | 3 × 3 | Cherry |
| 2 | 4 × 4 | Fig |
| 3 | 5 × 5 | Jackfruit |

### 🥦 Vegetable World

| Level | Grid | Answer |
|---|---:|---|
| 1 | 3 × 3 | Cabbage |
| 2 | 4 × 4 | Broccoli |
| 3 | 5 × 5 | Beetroot |

---

##  Built With

-  **Python**
-  **Tkinter** — GUI
-  **winsound** — sound effects
-  **OS module** — high-score file handling

The project uses Python's built-in modules, so no external Python packages are required.
---

##  Project Structure


```text
Pixel-Quest/
│
├── game.py
│
├── fruits.png
├── vegetables.png
│
├── fruit1.png
├── fruit2.png
├── fruit3.png
│
├── veg1.png
├── veg2.png
├── veg3.png
│
├── highscore.txt
│
└── README.md
```

---

##  Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/FabihaNurjina/Pixel_Quest.git
```

### 2. Open the project

```bash
cd Pixel_Quest
```

### 3. Run the game

```bash
python main.py
```

###  Windows Compatibility

Pixel Quest uses Python's `winsound` module for its sound effects, so the audio functionality is designed for **Windows**.

##  How to Play

1. Launch **Pixel Quest**.
2. Enter a world.
3. A hidden image will appear behind a grid.
4. Click a square to reveal part of the image.
5. Select your answer.
6. If you're wrong, reveal another square and try again.
7. Guess correctly before the timer reaches zero.
8. Complete all levels in the world.
9. Continue to the next world.
10. Try to beat your **high score!** 

##  How the Game Works

```text
              START
                │
                ▼
        Choose / Enter World
                │
                ▼
          Start a Level
                │
                ▼
       Hidden Image + Grid
                │
                ▼
         Reveal a Square
                │
                ▼
           Make a Guess
          /           \
      Correct        Incorrect
        │                │
        ▼                ▼
    Earn Points      Reveal More
        │                │
        ▼                └──────► Try Again
   Next Level
        │
        ▼
   World Complete
        │
        ▼
    Next World
        │
        ▼
   Grand Champion
```

##  Future Improvements

Potential future additions:

-  More themed worlds
-  More puzzle categories
-  Custom music and sound effects
-  Leaderboards
-  Player profiles
-  Game statistics
-  Difficulty modes
-  Animations and transitions
-  Online high-score system
-  More image-based challenges

##  Author

**Fabiha Nurjina**

##  Support

If you like this project, consider giving it a ⭐ on GitHub!
---

⭐ **If you enjoyed Pixel Quest, consider giving the repository a star!**
