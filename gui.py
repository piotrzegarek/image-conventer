from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Label, Frame, IntVar, DoubleVar, Scale
from tkinter import filedialog
from tkinter.messagebox import showinfo
from tkinter import ttk
from PIL import ImageTk,Image

from functions import (
    check_extension, resize_image, oil_painting_convert,
    cartoon_convert, pencil_convert, colored_pencil_convert,
)
from radiobtn import Radiobutton as RadioBtn


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/zegar/Desktop/PWPP/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class Application():
    def __init__(self):
        self.window = Tk()
        self.window.title("Photo Converter")
        self.window.geometry("1280x720")
        self.window.configure(bg = "#FFFFFF")
        self.create_background()
        self.create_upload_button()
        self.create_convert_button()
        self.create_save_button()
        self.create_image_canvas()
        self.create_radio_buttons()
        self.create_slider()
        self.window.resizable(False, False)

    def create_background(self):
        """ Create and place background image for the app."""
        self.canvas = Canvas(
            self.window,
            bg = "#FFFFFF",
            height = 720,
            width = 1280,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.background_img = PhotoImage(
            file=relative_to_assets("background.png"))
        self.background = self.canvas.create_image(
            640.0,
            360.0,
            image=self.background_img
        )

    def create_upload_button(self):
        """ Create and place button for uploading image files. """
        self.upload_btn_img = PhotoImage(
            file=relative_to_assets("upload_btn.png"))
        self.upload_btn = Button(
            image=self.upload_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.choose_file,
            relief="flat"
        )
        self.upload_btn.place(
            x=71.0,
            y=77.0,
            width=160.0,
            height=50.0
        )

    def create_convert_button(self):
        """ Create and place button for converting image files. """
        self.convert_btn_img = PhotoImage(
            file=relative_to_assets("convert_btn.png"))
        self.convert_btn = Button(
            image=self.convert_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.convert,
            relief="flat"
        )
        self.convert_btn.place(
            x=71.0,
            y=534.0,
            width=160.0,
            height=50.0
        )

    def create_save_button(self):
        """ Create and place button saving converted. """
        self.save_btn_img = PhotoImage(
            file=relative_to_assets("save_btn.png"))
        self.save_btn = Button(
            image=self.save_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_image,
            relief="flat"
        )
        self.save_btn.place(
            x=71.0,
            y=615.0,
            width=160.0,
            height=50.0
        )

    def create_image_canvas(self):
        """ Create and place canvas for displaying images. """
        self.border_color = Frame(self.window, bg="#9f71f0")
        img = Image.open(relative_to_assets("blank_bg.png"))
        img = img.resize((800,500), Image.ANTIALIAS)
        self.blank_img =  ImageTk.PhotoImage(img)
        self.blank_label = Label(self.window, image=self.blank_img)
        self.blank_label.place(
            x=350.0,
            y=100.0,
            width=800.0,
            height=500.0
        )
        self.border_color.place(
            x=348.0,
            y=98.0,
            width=804.0,
            height=504.0
        )

        self.image = None
        self.conv_image = None
        self.image_label = Label(self.window, image=self.blank_img, bg="#d2cbf5")
        self.image_label.place(
            x=350.0,
            y=100.0,
            width=800.0,
            height=500.0
        )

    def create_radio_buttons(self):
        self.convert_option = IntVar()
        self.convert_option.set(1)

        but_1 = RadioBtn(self.canvas, text="Oil painting", variable=self.convert_option, value=1,
                                fill="#102B72")
        but_1.put(71, 247)

        but_1 = RadioBtn(self.canvas, text="Cartoon", variable=self.convert_option, value=2,
                                fill="#102B72")
        but_1.put(71, 291)

        but_1 = RadioBtn(self.canvas, text="Sketch", variable=self.convert_option, value=3,
                                fill="#102B72")
        but_1.put(71, 335)

        but_1 = RadioBtn(self.canvas, text="Crayons", variable=self.convert_option, value=4,
                                fill="#102B72")
        but_1.put(71, 379)

        but_1 = RadioBtn(self.canvas, text="Pointillist Art", variable=self.convert_option, value=5,
                                fill="#102B72")
        but_1.put(71, 423)


    def choose_file(self):
        """ Open a file dialog to choose an image file. """
        ifile = filedialog.askopenfile(parent=self.window, mode='rb',title='Choose a file')
        if ifile is None:
            return
        if check_extension(ifile.name) is False:
            showinfo(
                title="Invalid File",
                message="Please select an image file"
            )
        else:
            self.display_image(ifile.name)
            self.conv_image = None

    def display_image(self, img_path: str):
        """ Display selected image in the label. """
        self.image = Image.open(img_path)

        resized_img = resize_image(self.image)
        uploaded_img = ImageTk.PhotoImage(resized_img)
        self.image_label.configure(image=uploaded_img)
        self.image_label.image=uploaded_img

    def convert(self):
        """ Convert the image and display it in the label. """
        if self.image is None:
            showinfo(
                title="No File",
                message="Please select an image file"
            )
            return
        else:
            self.get_converted_image()
            self.display_converted_image()

    def get_converted_image(self):
        """ Get the converted image based on selected conversion option. """
        if self.convert_option.get() == 1:
            self.conv_image = oil_painting_convert(self.image)
        elif self.convert_option.get() == 2:
            self.conv_image = cartoon_convert(self.image)
        elif self.convert_option.get() == 3:
            self.conv_image = pencil_convert(self.image)
        elif self.convert_option.get() == 4:
            self.conv_image = colored_pencil_convert(self.image)
        else:
            pass

    def display_converted_image(self):
        """ Display the converted image in the label. """
        resized_img = resize_image(self.conv_image)
        resized_conv_img = ImageTk.PhotoImage(resized_img)
        self.image_label.configure(image=resized_conv_img)
        self.image_label.image=resized_conv_img

    def save_image(self):
        """ Save converted image to a file. """
        if self.conv_image is None:
            showinfo(
                title="No File",
                message="Please convert an image first"
            )
            return
        else:
            f = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
            if f is None:
                return
            pil_img = self.conv_image.convert('RGB')
            pil_img.save(f.name)
            pil_img.close()

    def run(self):
        self.window.mainloop()
