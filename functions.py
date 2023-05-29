from PIL import Image
import cv2
import numpy as np

def check_extension(filename: str) -> bool:
    """ Check if the file has a valid extension

    Args:
        filename (str): The filename to check

    Returns:
        bool: True if the file has a valid extension, False otherwise
    """
    if filename == "" or filename is None:
        return False
    
    valid_extensions = ["jpg", "jpeg", "png"]

    # Get the file extension
    file_extension = filename.split(".")[-1]

    # Check if the file extension is valid
    if file_extension in valid_extensions:
        return True
    else:
        return False
    

def resize_image(img: Image) -> Image:
    """ Resize the image to fit the GUI frame.

    Args:
        img (Image): The image to resize

    Returns:
        Image: The resized image
    """
    if (img.size[0] > img.size[1]):
        base_width = 800
        wpercent = (base_width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        resized_img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    else:
        base_height = 500
        hpercent = (base_height/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        resized_img = img.resize((wsize, base_height), Image.Resampling.LANCZOS)

    return resized_img

def oil_painting_convert(img: Image):
    """ Convert the image to an oil painting. """
    img = convert_to_cv_format(img)
    # converted_img = cv2.xphoto.oilPainting(img, 7, 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    morph = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    result = cv2.normalize(morph,None,20,255,cv2.NORM_MINMAX)
    converted_img = convert_to_pil_format(result)

    return converted_img

def cartoon_convert(img: Image):
    """ Convert the image to a cartoon. """
    img = convert_to_cv_format(img)
    converted_img = cv2.stylization(img, sigma_s=60, sigma_r=0.07)
    converted_img = convert_to_pil_format(converted_img)

    return converted_img

def pencil_convert(img: Image):
    """ Convert the image to a pencil sketch. """
    img = convert_to_cv_format(img)
    pencil_sketch_img, _ = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05) 
    converted_img = convert_to_pil_format(pencil_sketch_img)

    return converted_img

def colored_pencil_convert(img: Image):
    """ Convert the image to a colored pencil sketch. """
    img = convert_to_cv_format(img)
    _, pencil_sketch_img = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    converted_img = convert_to_pil_format(pencil_sketch_img)

    return converted_img

def convert_to_cv_format(pil_img):
    """ Convert the image from PIL format to OpenCV format. """
    numpy_img = np.array(pil_img)
    opencv_image = cv2.cvtColor(numpy_img, cv2.COLOR_RGB2BGR) 
    
    return opencv_image

def convert_to_pil_format(opencv_image):
    """ Convert the image from OpenCV format to PIL format. """
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(opencv_image)

    return pil_img