import cv2 as cv
import numpy as np
import json
import math

# Примерные координаты:
coordinates_of_circles_RED_ = [(306, 418), (336, 389), (380, 319),
                              (303, 369), (347, 325), (379, 275),
                              (302, 304), (342, 262), (378, 227)]

coordinates_of_circles_GREEN_ = [(182, 333), (234, 397), (262, 418),
                                (177, 293), (213, 337), (258, 370),
                                (172, 240), (208, 273), (251, 310)]


coordinates_of_circles_BLUE_ = [(353, 215), (396, 175), (436, 140),
                               (355, 285), (405, 235), (430, 185),
                               (355, 338), (385, 310), (438, 228)]

coordinates_of_circles_ORANGE_ = [(222, 148), (260, 173), (302, 215),
                                 (222, 195), (260, 245), (310, 280),
                                 (225, 241), (280, 312), (312, 335)]

coordinates_of_circles_YELLOW_ = [(325, 155), (275, 120), (235, 88),
                                 (372, 115), (325, 80), (275, 61),
                                 (412, 82), (375, 55), (346, 37)]

coordinates_of_circles_WHITE_ = [(273, 251), (316, 210), (355, 178),
                                (224, 220), (268, 182), (324, 153),
                                (187, 191), (220, 165), (292, 132)]

coordinates_of_circles_RED = [(306, 418), (336, 389), (380, 319),
                              (303, 369), "red", (379, 275),
                              (302, 304), (342, 262), (378, 227)]

coordinates_of_circles_GREEN = [(182, 333), (234, 397), (262, 418),
                                (177, 293), "green", (258, 370),
                                (172, 240), (208, 273), (251, 310)]


coordinates_of_circles_BLUE = [(353, 215), (396, 175), (436, 140),
                               (355, 285), "blue", (430, 185),
                               (355, 338), (385, 310), (438, 228)]

coordinates_of_circles_ORANGE = [(222, 148), (260, 173), (302, 215),
                                 (222, 195), "orange", (310, 280),
                                 (225, 241), (280, 312), (312, 335)]

coordinates_of_circles_YELLOW = [(325, 155), (275, 120), (235, 88),
                                 (372, 115), "yellow", (275, 61),
                                 (412, 82), (375, 55), (346, 37)]

coordinates_of_circles_WHITE = [(273, 251), (316, 210), (355, 178),
                                (224, 220), "white", (324, 153),
                                (187, 191), (220, 165), (292, 132)]

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
    def __init__(self, index, sides, should_flip_image=False):
        self.camera = cv.VideoCapture(index)
        self.sides = sides
        self.should_flip_image = should_flip_image
        self.check_connection()

    def check_connection(self):
        if not self.camera.isOpened():
            raise ConnectionError

    def get_frame(self):
        ret, frame = self.camera.read()

        if not ret:
            raise ConnectionError

        #frame = cv.convertScaleAbs(frame, alpha=1.5, beta=1)
        if self.should_flip_image:
            frame = cv.flip(frame, 0)

        return frame

    def get_colors_array(self, side):
        colors = []
        coordinates_of_colors = COORDINATES_OF_CIRCLES[side]
        frame = self.get_frame()
        for coordinates in coordinates_of_colors:
            if type(coordinates) == str:
                color_array = coordinates
            else:
                # calibrating_array_red = []
                # calibrating_array_green = []
                # calibrating_array_blue = []
                coordinates = list(reversed(coordinates))
                color_array = self.get_color(frame, coordinates)
                #color_array = list(map(int, frame[*coordinates, [2, 1, 0]]))
                # for i in range(5):
                #     frame = self.get_frame()
                #     color = frame[*coordinates, [2, 1, 0]]
                #     calibrating_array_red.append(int(color[0]))
                #     calibrating_array_green.append(int(color[1]))
                #     calibrating_array_blue.append(int(color[2]))
                # color_array = [int(sum(calibrating_array_red) / 5),
                #                int(sum(calibrating_array_green) / 5),
                #                int(sum(calibrating_array_blue) / 5)]
            colors.append(color_array)
        return colors

    def get_color(self, frame, coordinates):
        offset = [-1, 0, 1]
        color_array = []
        for y_offset_index in range(3):
            for x_offset_index in range(3):
                y, x = coordinates[0] + offset[y_offset_index], coordinates[1] + offset[x_offset_index]
                color = frame[y, x, [2, 1, 0]]
                color_array.append(list(map(int, color)))
        color_array = self.get_average_values(color_array)
        return color_array
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

    def release(self):
        self.camera.release()


class Scanner:
    def __init__(self):
        self.upper_camera = Camera(2, ["yellow", "orange", "blue"])
        self.lower_camera = Camera(0, ["green", "red", "white"])

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
        self.upper_camera.calibrate_values()
        self.lower_camera.calibrate_values()

    def scan_cube(self):
        self.get_colors_values()
        lists_of_calibrated_colors_arrays = [self.yellow_value, self.blue_value, self.red_value,
                                             self.green_value, self.orange_value, self.white_value]
        colors_keys = ["y", "b", "r", "g", "o", "w"]
        cube = ""
        colors = [self.upper_camera.get_colors_array("yellow"),
                  self.upper_camera.get_colors_array("blue"),
                  self.lower_camera.get_colors_array("red"),
                  self.lower_camera.get_colors_array("green"),
                  self.upper_camera.get_colors_array("orange"),
                  self.lower_camera.get_colors_array("white")]
        for side in colors:
            for color in side:
                if type(color) == str:
                    color_value = color[0]
                else:
                    closest_list = find_closest_list(color, lists_of_calibrated_colors_arrays)
                    color_value = colors_keys[lists_of_calibrated_colors_arrays.index(closest_list)]
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

    def release_cameras(self):
        self.upper_camera.release()
        self.lower_camera.release()

def get_distance_between_lists(list_1, list_2):
    return math.sqrt(sum((first_list_color - second_list_color) ** 2 for first_list_color, second_list_color in zip(list_1, list_2)))

def find_closest_list(input_list, list_of_lists):
    closest_distance = float('inf')
    closest_list = []

    for current_list in list_of_lists:
        distance = get_distance_between_lists(input_list, current_list)
        if distance < closest_distance:
            closest_distance = distance
            closest_list = current_list

    return closest_list

def showing_frame(should_turn_on_second_camera):
    cap_1 = cv.VideoCapture(2)
    cap_2 = None
    if should_turn_on_second_camera:
        cap_2 = cv.VideoCapture(0)
        if not cap_2.isOpened():
            raise ConnectionError
    if not cap_1.isOpened():
        raise ConnectionError
    while True:
        #Capture frame-by-frame
        ret_1, frame_1 = cap_1.read()
        ret_2, frame_2 = None, None
        if should_turn_on_second_camera:
            ret_2, frame_2 = cap_2.read()

        # if frame is read correctly ret is True
        if not ret_1 :
            raise ConnectionError

        if should_turn_on_second_camera:
            if not ret_2:
                raise ConnectionError
        # Our operations on the frame come here
        #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Display the resulting frame
        #frame = cv.flip(frame, 1)
        # if flag:
        #     get_color(frame, coordinates_of_circles)
        #     flag = False
        for i in range(9):
            cv.circle(frame_2, coordinates_of_circles_WHITE_[i], 5, (0, 255, 0))
            cv.circle(frame_2, coordinates_of_circles_RED_[i], 5, (0, 255, 0))
            cv.circle(frame_2, coordinates_of_circles_GREEN_[i], 5, (0, 255, 0))
            cv.circle(frame_1, coordinates_of_circles_BLUE_[i], 5, (0, 255, 0))
            cv.circle(frame_1, coordinates_of_circles_ORANGE_[i], 5, (0, 255, 0))
            cv.circle(frame_1, coordinates_of_circles_YELLOW_[i], 5, (0, 255, 0))
            #if should_turn_on_second_camera:
            #    cv.circle(frame_2, coordinates_of_circles_BLUE[i], 5, (0, 255, 0))
        # if should_turn_on_second_camera:
        #     frame_2 = cv2.convertScaleAbs(frame_2, alpha=1.5, beta=0.8)
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
        frame_2 = cv.flip(frame_2, 0)
        # if should_turn_on_second_camera:
        #     frame_2 = cv.convertScaleAbs(frame_2, alpha=0.5, beta=0.5)
        # frame_1 = cv.convertScaleAbs(frame_1, alpha=0.5, beta=0.5)
        cv.imshow('frame_1', frame_1)
        if should_turn_on_second_camera:
            cv.imshow('frame_2', frame_2)
        if cv.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    cap_1.release()
    if should_turn_on_second_camera:
        cap_2.release()
    cv.destroyAllWindows()


showing_frame(True)
# scanner = Scanner()
# scanner.calibrate_values()
# scanner.release_cameras()





























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



