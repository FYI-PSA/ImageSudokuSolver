# ImageSudokuSolver
> Just as the name suggests, it looks at an image you save in it's directory (usually a screenshot or a screen snip, named 'screenshot.png'). Then it attempts to solve any Sudoku puzzles that might be on it. It can solve any Sudoku puzzle so no need to worry (even if they require bruteforce or have multiple answers. Even empty grids!)
> (Your image should still be good quality enough to be able to be recognised.)

## Install
> It is recommended that you create a new virtual environment using Python3.10 as the packages in this project are quite fragile and changing versions often leads to breaking changes in the code.

Steps:
1. Make a new **Python3.10** environment and activate it
```bash
python -m venv ImageSudokuSolver
cd ImageSudokuSolver
./Scripts/activate

```

2. Clone the repository  or  Download it and extract it and after extracting, change the name of the extracted folder from `ImageSudokuSolver-Stable` to `ImageSudokuSolver`
  - With Git clone:
```bash
git clone https://github.com/FYI-PSA/ImageSudokuSolver.git
cd ImageSudokuSolver

```
  - Without Git clone:
```bash
curl https://github.com/FYI-PSA/ImageSudokuSolver/archive/refs/heads/Stable.zip -OutFile Stable.zip
unzip Stable.zip
mv ImageSudokuSolver-Stable ImageSudokuSolver
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
