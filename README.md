# draughts-mcts

## Project Description

This project implements a draughts (checkers) game with a Monte Carlo Tree Search (MCTS) algorithm for the computer player's decision-making. The main component of the project is a Jupyter Notebook (`draughts_mcts.ipynb`), which likely contains the MCTS implementation and game simulations.

## Requirements

*   Python 3.x
*   Jupyter Notebook or JupyterLab
*   NumPy
*   Matplotlib
*   SciPy

## Installation

It is recommended to use a virtual environment to manage project dependencies.

1.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    ```

2.  **Activate the virtual environment:**

    *   On Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

3.  **Install the required packages:**

    You can create a `requirements.txt` file with the following content:

    ```
    numpy
    matplotlib
    scipy
    jupyter
    ```

    Then install the packages using pip:
    ```bash
    pip install -r requirements.txt
    ```
    Alternatively, you can install the packages individually:
    ```bash
    pip install numpy matplotlib scipy jupyter
    ```

## Running

To run the main part of the project, open and run the Jupyter Notebook:

```bash
jupyter notebook draughts_mcts.ipynb
```

Or if you are using JupyterLab:

```bash
jupyter lab draughts_mcts.ipynb
```

The `draughts.py` file contains the draughts game logic and can be used independently or as a module in the notebook. The `time_measuring.py` file contains tools for measuring function execution time, which can be useful for analyzing the performance of the MCTS algorithm.