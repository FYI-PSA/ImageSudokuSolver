# Image Sudoku Solver
> Just as the name suggests, it looks at an image you save in it's directory (usually a screenshot or a screen snip, named 'screenshot.png'). Then it attempts to solve any Sudoku puzzles that might be on it. It can solve any Sudoku puzzle so no need to worry (even if they require bruteforce or have multiple answers. Even empty grids!)
> (Your image should still be good quality enough to be able to be recognised.)

## Install
> When creating the new virtual environment, you **MUST** be using **Python3.10** as the packages in this project are quite annoyingly fragile and changing versions leads to breaking changes in the code or packages refusing to install.

Steps:
1. Make a new **Python3.10** environment and activate it. This step differs slightly between Linux and Windows:
  - **Windows**:
```bash
python -m venv ImageSudokuSolver
cd ImageSudokuSolver
./Scripts/activate

```

  - **Linux**:
    > Please first make sure that Python3.10 is installed on your system
    > Activating environments in Linux requires sourcing the activation files, not running them in bash. Use `source`
```bash
python3.10 -m venv ImageSudokuSolver
cd ImageSudokuSolver
source ./bin/activate

```

2. Clone the repository using the Git program   or   Download it and extract it.
  - With Git installed:
```bash
git clone https://github.com/FYI-PSA/ImageSudokuSolver.git
cd ImageSudokuSolver

```

  - Without Git installed:
    > You can manually do this step by visiting the url `https://github.com/FYI-PSA/ImageSudokuSolver/archive/refs/tags/Release.zip` and then unzipping it and renaming and shortening the name of the resulting folder to `ImageSudokuSolver`.
```bash
curl -LO https://github.com/FYI-PSA/ImageSudokuSolver/archive/refs/tags/Release.zip
unzip Release.zip
mv ImageSudokuSolver-Release ImageSudokuSolver
cd ImageSudokuSolver

```

3. Install the required packages to run this project
```bash
python -m pip install -r ./requirements.txt

```

> You can now run the project successfully.

## Usage
- Take a screenshot or a screen snip of your screen (as long as it clearly contains the grid and the grid is large enough to recognise the numbers.)
- Save the file in the same `ImageSudokuSolver` directory as the rest of the files.
- Run `main.py` (either by double clicking or by running it from a terminal)
