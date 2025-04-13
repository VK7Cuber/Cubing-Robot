import cv2
import numpy as np
import json

import cv2 as cv
#
# Примерные координаты:
coordinates_of_circles_RED = [(225, 165), (257, 200), (295, 245),
                              (222, 212), (255, 275), (297, 312),
                              (220, 260), (263, 340), (292, 367)]

coordinates_of_circles_GREEN = [(353, 245), (398, 225), (438, 200),
                                (345, 320), (400, 275), (436, 250),
                                (340, 380), (385, 350), (406, 334)]

coordinates_of_circles_BLUE = [(355, 130), (395, 161), (436, 229),
                               (355, 180), (405, 210), (438, 258),
                               (355, 245), (400, 280), (438, 313)]

coordinates_of_circles_ORANGE = [(230, 227), (277, 158), (310, 130),
                                 (230, 270), (270, 220), (312, 185),
                                 (227, 320), (265, 290), (305, 250)]

coordinates_of_circles_YELLOW = [(363, 88), (387, 105), (425, 142),
                                 (292, 94), (335, 125), (385, 165),
                                 (250, 120), (285, 155), (330, 195)]

coordinates_of_circles_WHITE = [(418, 368), (380, 400), (356, 419),
                                (380, 343), (337, 377), (281, 393),
                                (335, 310), (287, 343), (250, 370)]

# coordinates_of_circles_RED = [(225, 165), (257, 200), (295, 245),
#                               (222, 212), "red", (297, 312),
#                               (220, 260), (263, 340), (292, 367)]
#
# coordinates_of_circles_GREEN = [(353, 245), (398, 225), (438, 200),
#                                 (345, 320), "green", (436, 250),
#                                 (340, 380), (385, 350), (406, 334)]
#
# coordinates_of_circles_BLUE = [(355, 130), (395, 161), (436, 229),
#                                (355, 180), "blue", (438, 258),
#                                (355, 245), (400, 280), (438, 313)]
#
# coordinates_of_circles_ORANGE = [(230, 227), (277, 158), (310, 130),
#                                  (230, 270), "orange", (312, 185),
#                                  (227, 320), (265, 290), (305, 250)]
#
# coordinates_of_circles_YELLOW = [(363, 88), (387, 105), (425, 142),
#                                  (292, 94), "yellow", (385, 165),
#                                  (250, 120), (285, 155), (330, 195)]
#
# coordinates_of_circles_WHITE = [(418, 368), (380, 400), (356, 419),
#                                 (380, 343), "white", (281, 393),
#                                 (335, 310), (287, 343), (250, 370)]

COORDINATES_OF_CIRCLES = {"yellow": coordinates_of_circles_YELLOW,
                          "blue": coordinates_of_circles_BLUE,
                          "red": coordinates_of_circles_RED,
                          "green": coordinates_of_circles_GREEN,
                          "orange": coordinates_of_circles_ORANGE,
                          "white": coordinates_of_circles_WHITE}


class ScanError(Exception):
    pass


class ColorDetectionError(ScanError):
    pass


class Camera:
    def __init__(self, index, sides):
        self.camera = cv.VideoCapture(index)
        self.sides = sides
        self.check_connection()

    def check_connection(self):
        if not self.camera.isOpened():
            raise ConnectionError

    def get_frame(self):
        ret, frame = self.camera.read()

        if not ret:
            raise ConnectionError

        frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=1)
        return frame

    def get_colors_array(self, side):
        colors = []
        coordinates_of_colors = COORDINATES_OF_CIRCLES[side]
        for coordinates in coordinates_of_colors:
            if type(coordinates) == str:
                color_array = coordinates
            else:
                calibrating_array_red = []
                calibrating_array_green = []
                calibrating_array_blue = []
                coordinates = list(reversed(coordinates))
                for i in range(5):
                    frame = self.get_frame()
                    color = frame[*coordinates, [2, 1, 0]]
                    calibrating_array_red.append(int(color[0]))
                    calibrating_array_green.append(int(color[1]))
                    calibrating_array_blue.append(int(color[2]))
                color_array = [int(sum(calibrating_array_red) / 5),
                               int(sum(calibrating_array_green) / 5),
                               int(sum(calibrating_array_blue) / 5)]
            colors.append(color_array)
        return colors

    def get_average_values(self, color_array):
        red = []
        green = []
        blue = []
        for color in color_array:
            if type(color) != str:
                red.append(color[0])
                green.append(color[1])
                blue.append(color[2])
        avarage_color = [int(sum(red) / len(red)),
                         int(sum(green) / len(green)),
                         int(sum(blue) / len(blue))]
        return avarage_color

    def set_calibrated_value(self, side):
        avarage_color_value = self.get_average_values(self.get_colors_array(side))
        with open("calibrated_color_values.json", 'r') as json_file:
            data = json.load(json_file)
            data["colors"][side] = avarage_color_value
        with open("calibrated_color_values.json", 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def calibrate_values(self):
        for side in self.sides:
            self.set_calibrated_value(side)


class Scanner:
    def __init__(self):
        self.camera_yrg = Camera(2, ["yellow", "red", "green"])
        self.camera_obw = Camera(0, ["orange", "blue", "white"])

        self.yellow_value = None
        self.blue_value = None
        self.red_value = None
        self.green_value = None
        self.orange_value = None
        self.white_value = None

        self.sides = ["yellow", "red", "green", "orange", "blue", "white"]

    def get_colors_values(self):
        with open("calibrated_color_values.json", 'r') as json_file:
            data = json.load(json_file)
            self.yellow_value = data["colors"]["yellow"]
            self.blue_value = data["colors"]["blue"]
            self.red_value = data["colors"]["red"]
            self.green_value = data["colors"]["green"]
            self.orange_value = data["colors"]["orange"]
            self.white_value = data["colors"]["white"]

    def calibrate_values(self):
        self.camera_yrg.calibrate_values()
        self.camera_obw.calibrate_values()

    def scan_cube(self):
        self.get_colors_values()
        cube = ""
        colors = [*(self.camera_yrg.get_colors_array(color) for color in self.sides[:3]),
                  *(self.camera_obw.get_colors_array(color) for color in self.sides[3:])]
        print(colors)
        for side in colors:
            for color in side:
                if type(color) == str:
                    color_value = color[0]
                else:
                    if np.allclose(color, self.yellow_value, atol=20):
                        color_value = "y"
                    elif np.allclose(color, self.blue_value, atol=20):
                        color_value = "b"
                    elif np.allclose(color, self.red_value, atol=20):
                        color_value = "r"
                    elif np.allclose(color, self.green_value, atol=20):
                        color_value = "g"
                    elif np.allclose(color, self.orange_value, atol=20):
                        color_value = "o"
                    elif np.allclose(color, self.white_value, atol=20):
                        color_value = "w"
                    else:
                        color_value = "Error"
                cube += color_value
        return cube

    def get_cube_state(self):
        cube = self.scan_cube()
        error_iterations = 10
        while "Error" in cube:
            cube = self.scan_cube()
            error_iterations -= 1
            if error_iterations == 0:
                raise ColorDetectionError()
        return cube


def showing_frame():
    cap_1 = cv.VideoCapture(2)
    cap_2 = cv.VideoCapture(0)
    if not cap_1.isOpened() or not cap_2.isOpened():
        raise ConnectionError
    while True:
        #Capture frame-by-frame
        ret_1, frame_1 = cap_1.read()
        ret_2, frame_2 = cap_2.read()

        # if frame is read correctly ret is True
        if not ret_1 or not ret_2:
            raise ConnectionError
        # Our operations on the frame come here
        #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Display the resulting frame
        #frame = cv.flip(frame, 1)
        # if flag:
        #     get_color(frame, coordinates_of_circles)
        #     flag = False
        for i in range(9):
            cv.circle(frame_1, coordinates_of_circles_RED[i], 5, (0, 255, 0))
            cv.circle(frame_2, coordinates_of_circles_WHITE[i], 5, (0, 255, 0))
        frame_2 = cv2.convertScaleAbs(frame_2, alpha=1.5, beta=0.8)
        # coordinates = coordinates_of_circles_GREEN[0]
        # px = frame_1[coordinates[1], coordinates[0], [2,1,0]]
        # print(px)
        # print(type(px))
        # if 100 < px[0] < 125 and 60 < px[1] < 85 and 30 < px[2] < 60:
        #     print("Blue!")
        # elif 1 < px[0] < 20 and 80 < px[1] < 110 and 120 < px[2] < 140:
        #     print("Yellow!")
        # elif 10 < px[0] < 40 and 10 < px[1] < 40 and 100 < px[2] < 130:
        #     print("Red!")
        cv.imshow('frame_1', frame_1)
        cv.imshow('frame_2', frame_2)
        if cv.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    cap_1.release()
    cap_2.release()
    cv.destroyAllWindows()

#showing_frame()
scanner = Scanner()
print(scanner.scan_cube())
# import numpy as np
# import cv2
#
# COLOR_ROWS = 80
# COLOR_COLS = 250
#
# capture = cv2.VideoCapture(2)
# if not capture.isOpened():
#     raise RuntimeError('Error opening VideoCapture.')
#
# (grabbed, frame) = capture.read()
# snapshot = np.zeros(frame.shape, dtype=np.uint8)
# cv2.imshow('Snapshot', snapshot)
#
# colorArray = np.zeros((COLOR_ROWS, COLOR_COLS, 3), dtype=np.uint8)
# cv2.imshow('Color', colorArray)
#
#
# def on_mouse_click(event, x, y, flags, userParams):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         colorArray[:] = snapshot[y, x, :]
#         rgb = snapshot[165, 225, [2, 1, 0]]
#
#         # From stackoverflow/com/questions/1855884/determine-font-color-based-on-background-color
#         luminance = 1 - (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
#         if luminance < 0.5:
#             textColor = [0, 0, 0]
#         else:
#             textColor = [255, 255, 255]
#
#         cv2.putText(colorArray, str(rgb), (20, COLOR_ROWS - 20),
#                     fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=textColor)
#         cv2.imshow('Color', colorArray)
#
#
# cv2.setMouseCallback('Snapshot', on_mouse_click)
#
# while True:
#     (grabbed, frame) = capture.read()
#     cv2.imshow('Video', frame)
#
#     if not grabbed:
#         break
#
#     keyVal = cv2.waitKey(1) & 0xFF
#     if keyVal == ord('q'):
#         break
#     elif keyVal == ord('t'):
#         snapshot = frame.copy()
#         cv2.imshow('Snapshot', snapshot)
#
# capture.release()
# cv2.destroyAllWindows()
