# Chess App

A chess game project with a focus on dynamic board analysis and learning tools.

## Example

![Board themes](https://github.com/ChabanovX/chess/blob/main/board_variations.png)

## Structure

```
chess/
    engine/     # core board and piece logic
    ui/         # pygame interface
    network/    # socket server utilities
assets/         # images and sounds
scripts/        # helper entry points
```

## Run

### 1. Install the repo
```bash
git clone https://github.com/ChabanovX/chess
cd chess
```

### 2. Load the dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run main
```bash
python -m chess.ui.main
```

### 4. Run the network server
```bash
python -m chess.network.server
```

## Features

* Dynamic board analysis
* Learning mode with move suggestions and analysis
* Multiplayer support via socket server
* Customizable themes and sound effects

## Goals

* Create a new way of analyzing the board to help people learn chess faster
* Provide a user-friendly interface for players of all skill levels
* Implement a robust multiplayer system for playing with friends

## Current Status

* Project is in development, with a focus on building core features and functionality
* Contributions and feedback welcome!