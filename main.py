import copy
import math
import time
from collections import Counter
import colorama
from termcolor import colored
import sudokureader
import sudokuextractor


def gridprint(grid):
    widest = max([max([len(str(c)) for c in r]) for r in grid])  # "Cyclomatic complexity too high" from flake8. Probably wants me to use a switch-case
    for __, i in enumerate(grid):
        for _, j in enumerate(i):
            if j == 0:
                print(colored(j, 'dark_grey'), end='')
            elif j == 1:
                print(colored(j, 'red'), end='')
            elif j == 2:
                print(colored(j, 'blue'), end='')
            elif j == 3:
                print(colored(j, 'magenta'), end='')
            elif j == 4:
                print(colored(j, 'light_magenta'), end='')
            elif j == 5:
                print(colored(j, 'light_blue'), end='')
            elif j == 6:
                print(colored(j, 'yellow'), end='')
            elif j == 7:
                print(colored(j, 'white'), end='')
            elif j == 8:
                print(colored(j, 'light_red'), end='')
            elif j == 9:
                print(colored(j, 'light_yellow'), end='')
            else:
                print(colored(j, 'light_green'), end='')
            if _ == (len(i) - 1):
                continue
            print(' '*(widest-len(str(j))), end='')
            print(' ', end="")
            if ((_+1) % 3) == 0:
                print(' '*math.floor(widest*1.1), end='')
            print(' ', end="")
        if ((__+1) % 3) == 0:
            print('', end='\n\n')
        print('', end='\n')


def breakdowntoset(smalllistorstr):
    largerset = set()
    if isinstance(smalllistorstr, str):
        input = str(smalllistorstr).strip().lower()
    else:
        input = smalllistorstr
    if input == '' or input == []:
        return largerset
    for _ in input:
        if isinstance(_, int):
            largerset.add(_)
        elif _ == '-':
            continue
        elif isinstance(_, bool):
            raise Exception("Somehow a boolean array is passed to be broken into a set")
        else:
            try:
                largerset = largerset | (set(map(int, _.split('-'))))
            except ValueError:
                raise Exception(f"Somehow something that's not a bool, int, or number str, is passed to be broken into a set:\nItem: ({_}), Type: ({type(_)})")
    return largerset


# CONSTANTS
colorama.init()  # for using the colored library on windows machines.
global ALL, EMPTYGRID
M = 9
ALL = set(range(1, M+1))
CHECK_CELLS = [(0, 0), (1, 3), (2, 6), (3, 1), (4, 4), (5, 7), (6, 2), (7, 5), (8, 8)]  # Definitely mathematically reduntant and can be reduced.
# I don't want to do that though, too lazy. Deal with it, it's not slow enough to care about.
GRID = list([[0 for _ in range(M)] for _ in range(M)])
EMPTYGRID = copy.deepcopy(GRID)


def SolveByGrid(base) -> tuple:  # takes a base grid and tries to solve for lonely items. returns a candidate-filled kinda-solved grid and the normal kinda-solved grid
    global ALL
    grid = copy.deepcopy(base)
    candid = copy.deepcopy(grid)
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if item == 0:
                temp_ = row
                neighbours = copy.deepcopy(temp_)
                temp_ = [_r[j] for _r in grid]
                neighbours.extend(temp_)
                box_i = i // 3
                box_j = j // 3
                temp_ = []
                for i_, row_ in enumerate(grid[box_i*3:(box_i+1)*3]):
                    for j_, item_ in enumerate(row_[box_j*3:(box_j+1)*3]):
                        temp_.append(item_)
                neighbours.extend(temp_)
                neighbours = set(neighbours)
                neighbours.remove(0)
                possible = ALL - neighbours
                if len(possible) == 1:
                    grid[i][j] = next(iter(possible))
                    candid[i][j] = next(iter(possible))
                # elif len(possible) < 7 and len(possible) > 1:  # WHAT KIND OF IDIOT PUT THE LESS THAN 7 HERE WHILE I WAS FIRST MAKING THIS?!
                elif len(possible) > 1:
                    candid[i][j] = '-'.join([str(i) for i in iter(possible)])
    return (candid, grid)


def SolveByCandid(candidbase, gridbase) -> list:  # takes a candidate-containing grid and the normal grid and tries to solve based on being the only candidate for a number in a set. returns a kinda-solved normal grid
    global ALL
    candid = copy.deepcopy(candidbase)
    grid = copy.deepcopy(gridbase)
    for i, row in enumerate(candid):
        for j, item in enumerate(row):
            if not isinstance(item, int):
                itemsuperpos = set(map(int, item.split('-')))  # Never used, but I'm too afraid to remove this.
                neighbour_row = [k for (_, k) in enumerate(row) if (_ != j)]
                n_r = breakdowntoset(neighbour_row)
                neighbour_col = [r_[j] for (k, r_) in enumerate(candid) if (k != i) ]
                n_c = breakdowntoset(neighbour_col)
                box = []
                box_i = i // 3
                box_j = j // 3
                for i_, row_ in enumerate(candid[box_i*3:(box_i+1)*3]):
                    for j_, item_ in enumerate(row_[box_j*3:(box_j+1)*3]):
                        if i_ == (i % 3) and j_ == (j % 3):
                            continue
                        box.append(item_)
                n_b = breakdowntoset(box)
                # THIS OPERATION IS NOT GLOBAL
                # IT APPLIES SEPERATELY TO EACH LOCK
                r_r = ALL - n_r
                r_c = ALL - n_c
                r_b = ALL - n_b
                if len(r_r) == 1:
                    grid[i][j] = next(iter(r_r))
                if len(r_c) == 1:
                    grid[i][j] = next(iter(r_c))
                if len(r_b) == 1:
                    grid[i][j] = next(iter(r_b))
    return grid


def SimpleSolve(gridbase) -> tuple:  # takes a normal unsolved grid, and tries to solve it using the two functions above. returns a potentially condidate-containing grid and a potentially solved grid.
    global EMPTYGRID
    grid = copy.deepcopy(gridbase)
    candid = copy.deepcopy(grid)
    copygrid = copy.deepcopy(EMPTYGRID)
    copycandid = copy.deepcopy(EMPTYGRID)
    copytotal = copy.deepcopy(EMPTYGRID)
    firsttotal = True
    firstgrid = True
    firstcandid = True
    while copytotal != grid or firsttotal:
        firsttotal = False
        copytotal = copy.deepcopy(grid)
        while copygrid != grid or firstgrid:
            firstgrid = False
            copygrid = copy.deepcopy(grid)
            candid, grid = SolveByGrid(grid)
        # runs until SolveByGrid doesn't change grid
        while copycandid != grid or firstcandid:
            firstcandid = False
            copycandid = copy.deepcopy(grid)
            grid = SolveByCandid(candid, grid)
        # runs until SolveByCandid doesn't change grid
        candid, grid = SolveByGrid(grid)
    return (candid, grid)


def GuessworkSolve(gridbase, debug=False) -> tuple:  # solves the grid by trying the normal solve methods on it, then applying a brute force technique to any unsolved tiles and then trying itself again. takes an unsolved grid as input and returns a boolean for it was solvable and a hopefully solved grid.
    candid, grid = SimpleSolve(gridbase)
    if not CheckValidGrid(grid):
        return (False, grid)
    if debug:
        print(colored("[#] Debug turn:\n", "light_yellow"))
        gridprint(candid)
        print("")
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if item != 0:
                continue
            candidatestr = candid[i][j]
            if not isinstance(candidatestr, str):
                if debug:
                    print(colored("[#] *BEEP*! Reached a wrong answer, sorry!", "magenta"))
                return (False, copy.deepcopy(grid))
            candidates = breakdowntoset(candidatestr)

            # if len(candidates) == 0:  # I'm pretty sure this is impossible because if a set is of length less than one, the SolveByGrid doesn't assign it a candidate string, but leaves it as 0.
            #     if debug:  # But I'm still keeping this code in case I accidentally change something about that.
            #         print(colored("[#] *BEEP*! Reached a wrong answer, sorry!", "magenta"))  # This is definitely a sign of bad coding (lol): uncertainty of input type.
            #     return (False, copy.deepcopy(grid))

            for r_ in candid:  # Prevent the code from going down a spiral when already a grid is definitely unsolvable.
                for j_ in r_:
                    if j_ == 0:
                        return (False, copy.deepcopy(grid))

            candidates = list(candidates)
            candidates.sort()
            # if reaching this point:
            # a number on the grid is missing, and it has possible values as ints in an ordered list from small to large.
            for p in candidates:
                testgrid = []
                testgrid = copy.deepcopy(grid)
                testgrid[i][j] = p
                couldbesolved, answer = GuessworkSolve(testgrid, debug=debug)
                if couldbesolved and CheckValidGrid(answer):
                    return (True, answer)
            # it's impossible for it not to be one of the values that are possible for a number, so if reaching this point, automatically assume failure.
            if debug:
                print(colored("[#] Assuming failure.", "magenta"))
            return (False, copy.deepcopy(grid))
    return (CheckValidGrid(grid), copy.deepcopy(grid))


def CheckValidGrid(gridbase) -> bool:  # takes a solved or an unsolved grid and checks each row and column and box only once (9 total tiles) (using some tile coordinates written in the constants) for repeating numbers. returns True if no repeats and False if the grid was solved incorrectly.
    global CHECK_CELLS
    grid = copy.deepcopy(gridbase)
    for i, j in CHECK_CELLS:
        row = gridbase[i]
        item = row[j]
        row_neigh = [n for n in copy.deepcopy(row) if n != 0]
        col_neigh = [_r[j] for _r in grid if _r[j] != 0]
        box_i = i // 3
        box_j = j // 3
        box_neigh = []
        for i_, row_ in enumerate(grid[box_i*3:(box_i+1)*3]):
            for j_, item_ in enumerate(row_[box_j*3:(box_j+1)*3]):
                if item_ == 0:
                    continue
                box_neigh.append(item_)
        if row_neigh != []:
            c_row = Counter(row_neigh)
            if c_row[max(c_row, key=lambda k: c_row[k])] > 1:
                return False
        if col_neigh != []:
            c_col = Counter(col_neigh)
            if c_col[max(c_col, key=lambda k: c_col[k])] > 1:
                return False
        if box_neigh != []:
            c_box = Counter(box_neigh)
            if c_box[max(c_box, key=lambda k: c_box[k])] > 1:
                return False
    return True


def read_gridjpg_to_grid(kerasmodel, filename='screenshot.png') -> list:
    tile_images = sudokuextractor.process_image_file_to_list_of_polished_np_tiles(filename=filename)
    tiles = sudokureader.grayscale_numpy_tiles_list_to_predicted_integer_list(tiles=tile_images, model=kerasmodel)
    # print(tiles)
    grid = [tiles[i:i + 9] for i in range(0, 81, 9)]
    return (copy.deepcopy(grid))


def main(model) -> int:  # main thing with all of the main UX and styling going on. gets the time to solve, solves the grid, returns.
    global GRID
    GRID = read_gridjpg_to_grid(filename='screenshot.png', kerasmodel=model)
    st = time.time()
    print("\n")
    print(colored("Unsolved Grid:\n", "blue"))
    gridprint(GRID)
    print("\n")
    couldbesolved, GRID = GuessworkSolve(GRID, debug=False)  # no debug
    # couldbesolved, GRID = GuessworkSolve(GRID, debug=True)  # yes debug
    et = time.time()
    dt = round(et - st, 3)
    print(colored(f"Time to solve: {dt} seconds", "magenta"))
    print(colored(f"The final grid is {'CORRECT' if couldbesolved else 'INCORRECT'}\n\n\n", "green" if couldbesolved else "red"))
    if not couldbesolved:
        print(colored("There's an error in:  1. The image quality - 2. The puzzle configuration - 3. The program", "red"))
        print(colored("Try a clearer picture, more zoomed in and clearer digits, and an obvious square grid in your screenshot.", "red"))
        print(colored("If you still face this error, check the validty of your puzzles and if it's correct or the image keeps refusing, open an issue report on this project's GitHub", "magenta"))
        print(colored("Project GitHub Page: https://github.com/FYI-PSA/ImageSudokuSolver", "magenta"))
        print("\n")
        print(colored("One of the failed attempts:\n", "red"))
        gridprint(GRID)
        print("\n")
        return 1
    print("\n")
    print(colored("Solved Grid:\n", "green"))
    gridprint(GRID)
    print("\n")
    return 0


if __name__ == '__main__':
    AImodel = sudokureader.load_model()
    try:
        failmsg = 'That attempt failed.\nNext one...'
        if main(model=AImodel) == 1:
            print(failmsg)
        while input(colored("[>] Type 'EXIT' to close the program. Press enter to do another turn: ", "blue")).strip().lower() != 'exit':
            if main(model=AImodel) == 1:
                print(failmsg)
        print(colored("\n[>] Exit.\n\n", "light_blue"))
        exit(0)
    except KeyboardInterrupt:
        print(colored("\n\n[>] Exit.\n\n", "light_blue"))
        exit(0)


#######


# in the same "box" reside numbers when i // 3 and j // 3 is same:
# g = [[(i//3)+(j//3) for i in range(9)] for j in range(9)]
# g = [[(i+j)%10 for i in range(0, 9)] for j in range(0, 9)]
# gridprint(g)

# input("press enter to exit")
