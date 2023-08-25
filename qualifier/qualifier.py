import cv2
import numpy as np

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    # Set tile height and width
    tile_height: int = tile_size[0]
    tile_width: int = tile_size[1]

    # Check for valid ordering lists
    list_length: int = len(ordering)
    valid_ordering: bool = False

    if sorted(ordering) == list(range(list_length)) and list_length == len(range(list_length)):
        valid_ordering = True

    # Check for remainders
    tile_remainder_width: int = image_size[1] % tile_width
    tile_remainder_height: int = image_size[0] % tile_height

    tile_count_img: int = 0
    tile_count_file: int = 0

    # Count the number of tiles possible in image
    for y in range(0, image_size[0], tile_height):
        for x in range(0, image_size[1], tile_width):
            tile_count_img += 1
    # Count the number of tiles in the order file
    for order in ordering:
        tile_count_file += 1

    if (tile_remainder_height == 0 and tile_remainder_width == 0) and (tile_count_file == tile_count_img) and valid_ordering:
        return True
    else:
        return False

def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    image = cv2.imread(image_path)
    # Set the shape of the image
    height, width, _ = image.shape
    img_dimensions = (height, width)

    reformation: bool = valid_input(img_dimensions,tile_size,ordering)
    if reformation:
        # Divide the tiles
        tiles = []
        for y in range(0, height, tile_size[0]):
            for x in range(0, width, tile_size[1]):
                tile = image[y:y + tile_size[0], x:x + tile_size[1]]
                tiles.append(tile)

        # Print the order
        print(ordering)

        rearranged_tiles = []

        # Create a list of given order
        for order in ordering:
            rearranged_tiles.append(tiles[order])

        # Create a new image with rearranged tiles
        rearranged_image = np.zeros_like(image)
        x_offset = 0
        y_offset = 0
        for tile in rearranged_tiles:
            h, w, _ = tile.shape
            rearranged_image[y_offset:y_offset + h, x_offset:x_offset + w] = tile
            x_offset += tile_size[1]
            if x_offset >= width:
                x_offset = 0
                y_offset += tile_size[0]

        # Save the rearranged image
        cv2.imwrite(f'{out_path}', rearranged_image)
    else:
        raise ValueError("The tile size or ordering are not valid for the given image")

