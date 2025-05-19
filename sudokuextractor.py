import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import cv2


# def getfilenameinfo(fname: str) -> tuple:  # useless
#     splitname = fname.split('.')
#     ext = splitname[-1]
#     actualname = ''.join(splitname[0:-1])
#     return (actualname, ext)


# def grayscale_to_binary(image: np.ndarray, debug: bool = False, thresh: float = 0.3):
#     valuearr = np.asanyarray(image, dtype=np.uint8)
#     fractionarr = valuearr / 255.0  # it's a black and white image so the numbers are 0-255, so if I divide by this, it's gonna be 0-1
#     treshholded = np.where(fractionarr > thresh, 1.0, 0.0)
#     if debug:
#         treshhold_img = treshholded * 255.0
#         plt.imshow(treshhold_img, cmap='Greys')
#         plt.show()
#     return treshholded


def rgb_image_from_file(fname: str, debug: bool = False):
    img = Image.open(fname)
    img = img.convert('RGB')
    if debug:
        plt.imshow(img)
        plt.show()
    return img


def image_to_grayscale(rgb_img: np.ndarray, debug: bool = False):
    img = rgb_img.convert('L')
    if debug:
        plt.imshow(img, cmap='Greys')
        plt.show()
    return np.asarray(img, dtype=np.uint8)


def rgb_image_to_inverse_thresholded_grayscale(rgb_image: np.ndarray, debug: bool = False):
    # my solution to this section
    # firstthresh = grayscale_to_binary(image_to_grayscale(debug=True), debug=True, thresh=0.7) * 255.0
    # image_to_grayscale returns black in bg and white in fg
    threshhold, firstthresh = cv2.threshold(image_to_grayscale(rgb_image), 0.0, 255.0, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # otsu's method find a midrange average by averaging the most and the least (+ other math opts probably)
    # the inv_binary_threshhold just makes a black and white image with black in the background to threshhold at 50% with white in the background instead
    # much better than my grayscale_to_binary function, so I won't use that any longer.
    blurred = cv2.GaussianBlur(firstthresh, (3, 3), 1)
    if debug:
        plt.imshow(blurred, cmap='Greys')
        plt.show()
    threshhold, secondthresh = cv2.threshold(firstthresh, 0.0, 255.0, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if debug:
        plt.imshow(secondthresh, cmap='Greys')
        plt.show()
    if debug:
        plt.imshow(255.0 - secondthresh, cmap='Greys')
        plt.show()
    return secondthresh


def rectanlge_contours_from_inverse_threshholded_image(threshholded_img: np.ndarray, debug: bool = False) -> list:
    # find contours
    contours = cv2.findContours(threshholded_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    rectangles = []
    for c in contours:
        # get the information of the contour box
        x, y, w, h = cv2.boundingRect(c)
        # if w*h > 1024:  # larger area than a 32 x 32 square
        if (w*h) > 49:  # larger area than a 7 x 7 square
            rectangles.append(cv2.boundingRect(c))
    if debug:
        print(rectangles)
    return rectangles


def largest_square_bounding_from_list_of_rectanlges(rectangles: list, debug: bool = False) -> tuple:
    # find (almost) square looking boxes out of the contours
    squares = []
    for r in rectangles:
        w = r[2]
        h = r[3]
        # if w > 0.9*h and w < 1.1*h:  # 10% is too much, changing it to only 7%
        if (w > (0.93*h)) and (w < (1.07*h)):
            squares.append(r)
    if squares == []:
        if rectangles == []:
            raise Exception("Image didn't contain any clear rectangular object. Try making it clearer.") 
            exit(1)
        raise Exception("Image had rectangles, but didn't have any shapes almost resembling a square or a grid. Try making it clearer.")
        exit(1)
    largest_square = max(squares, key=lambda s: s[2])
    if debug:
        x, y, w, h = largest_square
        print(f"x: {x}   y: {y}   width: {w}   height : {h}")
    return largest_square


def ensure_square_boundary(semisqaure_boundary: tuple) -> tuple:  # makes it fully equal if they're off by a tiny bit
    x, y, w, h = semisqaure_boundary
    delta = abs(w-h)
    ratio = max([delta/w, delta/h])
    if ratio < 0.1:  # this is just in case a rectangle gets passed to it for some reason
        w = max([w, h])  # increase the lower one, because it's easier to read with wall noise than to read half a digit
        h = w
    return (x, y, w, h)


def rgb_to_bgr(rgb_img: np.ndarray) -> np.ndarray:
    return np.array(rgb_img, dtype=np.uint8)[:, :, ::-1].copy()


def draw_boundary_to_new_mask(bounding_rectangle: tuple, rgb_original_img: np.ndarray) -> np.ndarray:
    bgr_img = rgb_to_bgr(rgb_original_img)
    x, y, w, h = bounding_rectangle
    mask = np.ones(bgr_img.shape[:2], dtype=np.uint8) * 255
    cv2.rectangle(mask, (x, y), (x+w, y+h), (0, 0, 255), -1)
    return mask


def draw_mask_to_original_image(mask: np.ndarray, rgb_original_img: np.ndarray) -> None:
    bgr_img = rgb_to_bgr(rgb_original_img)
    res_final = cv2.bitwise_and(bgr_img, bgr_img, mask=cv2.bitwise_not(mask))
    final_img = cv2.cvtColor(res_final, cv2.COLOR_BGR2RGB)
    plt.title('the grid mask on the original image')
    plt.imshow(rgb_original_img)
    plt.imshow(0mask)
    plt.imshow(final_img)
    plt.show()


def extract_square_boundary_to_image(square_bounding: tuple, rgb_original_img: np.ndarray, debug: bool = True) -> np.ndarray:
    x, y, w, h = square_bounding
    square = np.asarray(rgb_original_img, dtype=np.uint8)[y:y+h, x:x+h]
    square = Image.fromarray(square)
    if debug:
        plt.title('the final recognised largest square grid')
        plt.imshow(square)
        plt.show()
    return square


def split_square_to_81(square_image: Image.Image) -> list:
    image = np.asarray(square_image, dtype=np.uint8)
    side = square_image.shape[0]
    tileside = side / 9  # don't round yet. use round() after multiplying, to be accurate.
    tiles = []
    for j in range(0, 9):
        for i in range(0, 9):
            i_s, i_e = i, i+1
            j_s, j_e = j, j+1
            ys = round(tileside * j_s)
            ye = round(tileside * j_e)
            xs = round(tileside * i_s)
            xe = round(tileside * i_e)
            tiles.append(image[ys:ye, xs:xe])
    return tiles


def remove_border_pixels(grayscale_image: np.ndarray, margin_percent=5) -> np.ndarray:
    imgarr = np.asarray(grayscale_image, dtype=np.uint8)
    side = width = height = imgarr.shape[0]
    margin = round(margin_percent*side/100)
    cropbox = (margin, margin, width - (2 * margin), height - (2 * margin))
    gray = Image.fromarray(imgarr)
    borderless_img = gray.crop(cropbox)
    return np.asarray(borderless_img, dtype=np.uint8)


def resize_tile(grayscale_tile: np.ndarray) -> np.ndarray:
    tile = Image.fromarray(grayscale_tile, mode='L')
    tinytile = tile.resize((28, 28), Image.LANCZOS)
    return np.asarray(tinytile, dtype=np.uint8)


def clean_tile(grayscale_tile: np.ndarray) -> np.ndarray:
    borderless_tile: np.ndarray = remove_border_pixels(grayscale_tile, margin_percent=7)
    resized_borderless: np.ndarray = resize_tile(borderless_tile)
    return resized_borderless


def process_image_file_to_list_of_polished_np_tiles(filename: str) -> list:
    rgb_image = rgb_image_from_file(filename)
    threshholded_grayscale_image = rgb_image_to_inverse_thresholded_grayscale(rgb_image, debug=False)
    rectangle_boxes = rectanlge_contours_from_inverse_threshholded_image(threshholded_grayscale_image, debug=False)
    
    # for debugging purposes
    for b in rectangle_boxes:
        rectangular_mask = draw_boundary_to_new_mask(b, rgb_image)
        draw_mask_to_original_image(rectangular_mask, rgb_image)

    boundingbox_square = largest_square_bounding_from_list_of_rectanlges(rectangle_boxes, debug=False)
    corrected_boundary = ensure_square_boundary(boundingbox_square)  # ensures that width and height are the exact same number, by exanding the smaller one (if they're close to the shape of a square)
    square_image = extract_square_boundary_to_image(corrected_boundary, rgb_image, debug=False)
    
    # square_mask = draw_boundary_to_new_mask(corrected_boundary, rgb_image)
    # draw_mask_to_original_image(square_mask, rgb_image)  # This is a nice tool but it acts more as a debug because it's not useful
    
    grid = square_image
    inverse_clean_grid = rgb_image_to_inverse_thresholded_grayscale(grid, debug=False)
    borderless_inverse_clean_grid = remove_border_pixels(inverse_clean_grid, margin_percent=0.5)
    tiles: list = split_square_to_81(borderless_inverse_clean_grid)
    clean_tiles: list = list(map(clean_tile, tiles))
    
    return clean_tiles


def main() -> None:
    filename = 'screenshot.png'
    tile_images = process_image_file_to_list_of_polished_np_tiles(filename=filename)
    print(len(tile_images))


if __name__ == '__main__':
    main()
