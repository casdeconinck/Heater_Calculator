from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import time


class Heater:

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
        # to adjust: position of coreldraw app on desktop
        # make sure coreldraw opens on your PC (not separate screen) and it is taking full width/height of the screen
        self.mouse.position = (568, 1059)
        self.mouse.click(Button.left, 2)
        time.sleep(8)
        # press "new file"
        self.mouse.position = (14, 58)
        self.mouse.click(Button.left, 1)
        time.sleep(2)
        # press "ok" for settings of new file
        self.mouse.position = (1028, 717)
        self.mouse.click(Button.left, 1)
        time.sleep(2)
        # presses "freehand tool"
        self.mouse.position = (26, 275)
        self.mouse.click(Button.left, 1)
        time.sleep(1)
        # presses "2-point line" under "freehand tool"
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
        # to adjust: mouse goes to X coordinate (upper left box)
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
        # to adjust: mouse goes to Y coordinate (upper left box)
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
        # to adjust: mouse goes to height setting in upper left corner
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
        # to adjust: change thickness of a line in properties tab
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
        # to adjust: mouse goes to width settings of an element in upper left corner
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

    def go_to_transform_tab(self):
        with self.keyboard.pressed(Key.alt):
            self.keyboard.press(Key.f7)
        time.sleep(0.4)
        with self.keyboard.pressed(Key.alt):
            self.keyboard.press(Key.f7)
        time.sleep(0.4)

    def transform_x_cor(self, x):
        self.mouse.position = (1689, 221)
        time.sleep(0.5)
        self.mouse.click(Button.left, 2)
        time.sleep(0.4)
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)
        self.mouse.click(Button.left, 2)
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)
        time.sleep(0.4)
        new_x = x
        if "." in x:
            new_x = x.replace(".", ",")
        self.keyboard.type(new_x)

    def transform_y_cor(self, y):
        self.mouse.position = (1689, 250)
        time.sleep(0.5)
        self.mouse.click(Button.left, 2)
        time.sleep(0.5)
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)
        self.mouse.click(Button.left, 2)
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)
        time.sleep(0.4)
        new_y = y
        if "." in y:
            new_y = y.replace(".", ",")
        self.keyboard.type(new_y)

    def select_everything(self):
        self.mouse.position = (1402, 290)
        self.mouse.click(Button.left, 1)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('a')
            self.keyboard.release('a')

    def transform_copies(self, c):
        self.mouse.position = (1693, 308)
        time.sleep(0.8)
        self.mouse.click(Button.left, 2)
        time.sleep(0.5)
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)
        time.sleep(0.4)
        new_c = c
        if "." in c:
            new_c = c.replace(".", ",")
        self.keyboard.type(new_c)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(5)

    def go_back_to_properties_tab(self):
        self.mouse.position = (1402, 290)
        self.mouse.click(Button.left, 1)
        time.sleep(0.4)
        with self.keyboard.pressed(Key.alt):
            self.keyboard.press(Key.enter)
        time.sleep(0.4)
        with self.keyboard.pressed(Key.alt):
            self.keyboard.press(Key.enter)
        time.sleep(0.4)

    def silver_fingers(self, fingers_width, fingers_length: float, height: float, margin_H: float, busbar_width: float,
                       square_height, margin_W):
        self.draw_line_horizontal()
        time.sleep(0.5)
        self.adjust_width_of_non_lines(str(fingers_length-0.5*margin_W))
        time.sleep(0.5)
        self.adjust_width(str(fingers_width))
        time.sleep(0.5)

        xcor1 = 30 + fingers_length / 2 + busbar_width / 2 - 0.6 * margin_W
        ycor1 = 200 + float(height) / 2 - margin_H + fingers_width / 2
        self.adjust_y(str(ycor1))
        self.adjust_x(str(xcor1))

        xcor2 = 30 + fingers_length / 2 + (busbar_width / 2) + 0.6 * margin_W
        ycor2 = 200 + float(height) / 2 - margin_H - fingers_width / 2 - square_height
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('c')
            self.keyboard.release('c')
        time.sleep(0.3)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('v')
            self.keyboard.release('v')
        time.sleep(0.3)
        self.adjust_y(str(ycor2))
        self.adjust_x(str(xcor2))

    def create_busbar(self, x: str, height, busbar_width):
        self.mouse.position = (26, 275)
        self.mouse.click(Button.left, 1)
        time.sleep(0.5)
        self.mouse.position = (69, 289)
        self.mouse.click(Button.left, 1)
        time.sleep(0.5)
        self.draw_line()
        self.adjust_x(x)
        self.adjust_y("200")
        self.adjust_height(height)
        self.adjust_width(busbar_width)
