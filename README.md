# Catto-Run (Pygame)

A simple endless-runner featuring a cute cat, written with [Pygame](https://www.pygame.org/).

## Quick Start

```bash
# 1. Create & activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the game
python game.py
```

## Code Structure

- `game.py` – main entry point. Holds the `Game` loop and parallax background.
- `player.py` – `Player` sprite with jump & animation states.
- `coin.py` – collectible `Coin` sprite.
- `config.py` – tunable constants (screen size, asset folders, gameplay values).
- `layers/`, `sprite/`, `coins/` – image assets.
- `stepWise/` – earlier step-by-step prototypes (kept for reference).

## Controls

- **Right Arrow** – Move forward.
- **Space / W / Up Arrow** – Jump.
- **ESC / Window close** – Quit.

## Contributing

Pull requests are welcome! Feel free to open an issue to discuss improvements or new features.
