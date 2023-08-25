import cv2
from qualifier import valid_input,rearrange_tiles

# Load the image and order
image_path = './images/secret_image2_scrambled.png'
order_path = './images/secret_image2_order.txt'
rearranged_img_path = './rearranged_image.png'
image = cv2.imread(image_path)
with open(order_path, "r") as file:
    # Read lines and convert to integers
    order_list = [int(line.strip()) for line in file]

# Get the dimensions of the image
height, width, _ = image.shape
img_dimensions = (height, width)
tile_dimensions = (20, 20)

print(f"Height and Width of image:{img_dimensions}")

# Set tile height and width
tile_height = tile_dimensions[0]
tile_width = tile_dimensions[1]

reformation: bool = valid_input(img_dimensions,tile_dimensions,order_list)

if reformation:
   rearrange_tiles(image_path,tile_dimensions,order_list,rearranged_img_path)
else:
    print(f"Reformation not possible")
