from tkinter import Canvas

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

class Radiobutton:
    def __init__(self, canvas, text="", variable=None, value=0, radius=10,
                 fill="black"):
        self.canvas = canvas
        self.variable = variable
        self.fill = fill
        self.text = text
        self.value = value
        self.radius = radius

        self.variable.trace("w", self.redraw)

        self.circle = None

    def put(self, x, y):
        self.x = x
        self.y = y
        self.canvas.create_circle(x, y, self.radius, outline=self.fill)
        self.canvas.create_text(x + 2*self.radius, y, text=self.text,
                                fill=self.fill, anchor="w",  font=("RobotoRoman Bold", 20 * -1))
        self.redraw()
        self.canvas.bind("<Button-1>", self.select, add=True)

    def select(self, event):
        if (self.x - event.x)**2 + (self.y - event.y)**2 <= self.radius**2:
            self.variable.set(self.value)
            self.redraw()

    def create_circle(self):
        self.circle = self.canvas.create_circle(self.x, self.y, self.radius-4,
                                                outline=self.fill,
                                                fill=self.fill)

    def redraw(self, *args):
        if self.value == self.variable.get():
            if self.circle is None:
                self.create_circle()
        else:
            if self.circle is not None:
                self.canvas.delete(self.circle)
                self.circle = None
