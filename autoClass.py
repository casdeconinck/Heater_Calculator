from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import time
import keyboard


class Busbar:

    def __init__(self, height, width, busbar_width):
        self.height = height
        self.width = width
        self.busbar_width = busbar_width
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.last_xcor = 645
        self.last_ycor = 395

    def open_corel(self):
        # also sets up for drawing a line
        self.mouse.position = (568, 1059)
        self.mouse.click(Button.left, 2)
        time.sleep(8)
        self.mouse.position = (14, 58)
        self.mouse.click(Button.left, 1)
        time.sleep(2)
        self.mouse.position = (1028, 717)
        self.mouse.click(Button.left, 1)
        time.sleep(1)
        self.mouse.position = (26, 275)
        self.mouse.click(Button.left, 1)
        time.sleep(1)
        self.mouse.position = (69, 289)
        self.mouse.click(Button.left, 1)
        time.sleep(1)

    def draw_line(self):
        self.mouse.position = (809, 337)
        time.sleep(0.5)

        self.mouse.press(Button.left)
        time.sleep(0.5)
        self.mouse.move(0, 100)
        time.sleep(0.5)
        self.mouse.release(Button.left)

    def draw_line_horizontal(self):
        self.mouse.position = (809, 337)
        time.sleep(0.5)
        self.mouse.press(Button.left)
        time.sleep(0.5)
        self.mouse.move(100, 0)
        time.sleep(0.5)
        self.mouse.release(Button.left)

    def adjust_x(self, x: str):
        self.mouse.position = (79, 89)
        time.sleep(0.4)
        self.mouse.click(Button.left, 2)
        time.sleep(0.5)
        new_x = x
        if "." in x:
            new_x = x.replace(".", ",")
        self.keyboard.type(new_x)

        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def adjust_y(self, y: str):
        self.mouse.position = (83, 104)
        time.sleep(0.4)
        self.mouse.click(Button.left, 2)
        time.sleep(0.5)
        new_y = y
        if "." in y:
            new_y = y.replace(".", ",")
        self.keyboard.type(new_y)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def adjust_height(self, h: str):
        self.mouse.position = (188, 104)
        time.sleep(0.4)
        self.mouse.click(Button.left, 2)
        time.sleep(0.5)
        new_h = h
        if "." in h:
            new_h = h.replace(".", ",")
        self.keyboard.type(new_h)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def adjust_width(self, w: str):
        self.mouse.position = (1605, 234)
        time.sleep(0.4)
        self.mouse.click(Button.left, 2)
        time.sleep(0.5)
        new_w = w
        if "." in w:
            new_w = w.replace(".", ",")
        self.keyboard.type(new_w)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def copy_paste(self, x, y):
        self.last_xcor = x
        self.last_ycor = y
        time.sleep(0.4)
        self.mouse.position = (x, y)
        self.mouse.click(Button.left, 1)
        time.sleep(1)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('c')
            self.keyboard.release('c')
        time.sleep(0.5)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('v')
            self.keyboard.release('v')

    def adjust_width_of_non_lines(self, width: str):
        self.mouse.position = (178, 86)
        time.sleep(0.4)
        self.mouse.click(Button.left, 2)
        time.sleep(0.5)
        new_width = width
        if "." in width:
            new_width = width.replace(".", ",")
        self.keyboard.type(new_width)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def scallop(self, fingers_width):
        scallop = 4.2
        self.mouse.position = (16, 323)
        time.sleep(0.2)
        self.mouse.click(Button.left)
        time.sleep(0.2)
        self.mouse.position = (148, 284)
        self.mouse.press(Button.left)
        time.sleep(0.5)
        self.mouse.move(10, 10)
        time.sleep(0.5)
        self.mouse.release(Button.left)
        self.adjust_height("10")
        self.adjust_width_of_non_lines("10")
        time.sleep(0.2)
        self.mouse.position = (1628, 153)
        self.mouse.click(Button.left, 1)
        time.sleep(0.5)
        self.mouse.position = (1630, 208)
        self.mouse.click(Button.left, 1)
        time.sleep(0.5)
        self.mouse.position = (1597, 152)
        self.mouse.click(Button.left, 1)
        time.sleep(0.5)
        self.mouse.position = (1888, 444)
        self.mouse.click(Button.left, 1)
        time.sleep(0.5)
        self.mouse.position = (1663, 242)
        self.mouse.click(Button.left, 2)
        self.keyboard.type("4,2")
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(0.5)
        self.mouse.position = (1887, 264)
        time.sleep(0.5)
        self.mouse.click(Button.left, 1)
        width_height = scallop/((1/fingers_width)*1.25)
        time.sleep(0.5)
        self.adjust_height(str(width_height))
        time.sleep(0.5)
        self.adjust_width_of_non_lines(str(width_height))

        # Start with a square of 10x10 and apply scallop,
        # after this adjust the width of scallop: 4,2/((1/fingers_width)*1,25)

    def silver_fingers(self, fingers_width, fingers_length: float, squares_height, height: float, margin_H: float,
                       busbar_width: float, square_height, space_height, margin_W):
        self.draw_line_horizontal()
        time.sleep(0.5)
        self.adjust_width_of_non_lines(str(fingers_length))
        time.sleep(0.5)
        self.adjust_width(str(fingers_width))
        time.sleep(0.5)
        y_top = 0
        y_bottom = 0
        for i in range(0, 2*squares_height):
            if keyboard.is_pressed("space"):
                time.sleep(10)
                break

            if i % 2 == 0:
                x = 30 + fingers_length/2 + busbar_width/2 - 0.5*margin_W
                if i == 0:
                    ycor_t = 200 + float(height)/2 - margin_H + fingers_width/2
                else:
                    time.sleep(0.3)
                    with self.keyboard.pressed(Key.ctrl):
                        self.keyboard.press('c')
                        self.keyboard.release('c')
                    time.sleep(0.3)
                    with self.keyboard.pressed(Key.ctrl):
                        self.keyboard.press('v')
                        self.keyboard.release('v')
                    time.sleep(0.3)
                    ycor_t = y_top - square_height - space_height
                self.adjust_y(str(ycor_t))
                self.adjust_x(str(x))
                y_top = ycor_t
            else:
                x = 30 + fingers_length / 2 + (busbar_width / 2) + 0.5*margin_W
                time.sleep(0.3)
                with self.keyboard.pressed(Key.ctrl):
                    self.keyboard.press('c')
                    self.keyboard.release('c')
                time.sleep(0.3)
                with self.keyboard.pressed(Key.ctrl):
                    self.keyboard.press('v')
                    self.keyboard.release('v')
                time.sleep(0.3)
                if i == 1:
                    ycor_b = 200 + float(height)/2 - margin_H - fingers_width/2 - square_height
                else:
                    ycor_b = y_bottom - square_height - space_height
                self.adjust_y(str(ycor_b))
                self.adjust_x(str(x))
                y_bottom = ycor_b