# Connect 4 AI

Welcome to the Connect 4 AI repository! This project is an implementation of a classic Connect 4 game with an AI opponent capable of challenging human players. Utilizing algorithms and optimization techniques from CS152, this AI adapts to different game stages with strategic depth and efficiency.

## Features

- **Dynamic AI Difficulty**: AI adapts its search depth based on the game state.
- **Minimax Algorithm**: Employs a Minimax algorithm with alpha-beta pruning for optimal play.
- **Iterative Deepening**: Enhances performance by dynamically adjusting the search depth.
- **Transposition Table**: Optimizes memory usage and search speed by storing board states.
- **Pygame Interface**: A simple and interactive GUI for playing the game.

## Installation

To get started with Connect 4 AI, clone this repository and ensure you have Python and Pygame installed.

```bash
git clone https://github.com/Nathnaelc/CS152_Connect4AI.git
pip install -r requirements.txt
python3 Connect_4_Main_Version.py
```

## Usage

Run the game using Python from the command line:

```bash
python connect4_main.py
```

Follow the on-screen prompts to start the game against the AI.

## Testing

The repository includes scripts for testing AI performance under various scenarios:

## Testing

The repository includes a comprehensive suite of tests designed to validate the AI's performance and robustness across different scenarios:

- `test_adaptability_variable_boards.py`: Assesses the AI's adaptability to various board sizes, ensuring consistent strategy application regardless of the playing field's dimensions.

- `test_connect4.py`: Runs a series of games to test the core functionality of the Connect 4 game logic, validating that all game rules are correctly enforced and that win detection is accurate.

- `test_decision_making_quality.py`: Evaluates the quality of decisions made by the AI by simulating games and comparing the AI's moves against a set of benchmark outcomes.

- `test_depth_efficiency.py`: Measures the efficiency of the AI's search algorithm at different depths, highlighting the balance between decision-making quality and computational time.

- `test_evaluation_function.py`: Validates the evaluation function that guides the AI's move selection, ensuring that the heuristic accurately reflects the desirability of game states.

These descriptions are aimed to be concise yet informative, offering clear insight into the purpose and execution of each test.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.
