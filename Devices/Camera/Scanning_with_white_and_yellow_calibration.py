import cv2 as cv
import numpy as np
import json
import math
from typing import List, Tuple, Dict, Optional

# Coordinate arrays for scanning (with string values for center positions)
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

# Coordinate arrays for calibration (without string values)
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

COORDINATES_OF_CIRCLES = {
    "yellow": coordinates_of_circles_YELLOW,
    "blue": coordinates_of_circles_BLUE,
    "red": coordinates_of_circles_RED,
    "green": coordinates_of_circles_GREEN,
    "orange": coordinates_of_circles_ORANGE,
    "white": coordinates_of_circles_WHITE
}

COORDINATES_OF_CIRCLES_CALIBRATION = {
    "yellow": coordinates_of_circles_YELLOW_,
    "blue": coordinates_of_circles_BLUE_,
    "red": coordinates_of_circles_RED_,
    "green": coordinates_of_circles_GREEN_,
    "orange": coordinates_of_circles_ORANGE_,
    "white": coordinates_of_circles_WHITE_
}

# Color mapping for output
COLOR_MAPPING = {
    "yellow": "y",
    "blue": "b",
    "red": "r",
    "green": "g",
    "orange": "o",
    "white": "w"
}


class ScanError(Exception):
    """Base exception for scanning errors"""
    pass


class ColorDetectionError(ScanError):
    """Exception raised when color detection fails"""
    pass


class CameraConnectionError(ScanError):
    """Exception raised when camera connection fails"""
    pass


class Camera:
    def __init__(self, index: int, sides: List[str], should_flip_image: bool = False):
        """
        Initialize camera with specified index and sides to scan

        Args:
            index: Camera device index
            sides: List of cube sides this camera scans
            should_flip_image: Whether to flip the image vertically
        """
        self.camera = cv.VideoCapture(index)
        self.sides = sides
        self.should_flip_image = should_flip_image
        self.check_connection()

    def check_connection(self):
        """Check if camera is properly connected"""
        if not self.camera.isOpened():
            raise CameraConnectionError(f"Failed to open camera at index {self.camera.get(cv.CAP_PROP_POS_FRAMES)}")

    def get_frame(self):
        """Capture and return a frame from the camera"""
        ret, frame = None, None
        for i in range(20):
            ret, frame = self.camera.read()

        if not ret:
            raise CameraConnectionError("Failed to read frame from camera")

        if self.should_flip_image:
            frame = cv.flip(frame, 0)

        return frame

    def get_colors_array(self, side: str) -> List[str]:
        """
        Get color array for a specific side of the cube

        Args:
            side: Name of the cube side to scan

        Returns:
            List of color strings for each position on the face
        """
        colors = []
        coordinates_of_colors = COORDINATES_OF_CIRCLES[side]
        frame = self.get_frame()

        for coordinates in coordinates_of_colors:
            if isinstance(coordinates, str):
                # Center position - use predefined color
                colors.append(coordinates)
            else:
                # Edge and corner positions - detect color
                coordinates = list(reversed(coordinates))  # Convert to (y, x) format
                detected_color = self.get_color(frame, coordinates)
                colors.append(detected_color)

        return colors

    def get_color(self, frame, coordinates: Tuple[int, int]) -> str:
        """
        Detect color at specific coordinates using averaging method

        Args:
            frame: Camera frame
            coordinates: (y, x) coordinates to sample

        Returns:
            Detected color string
        """
        # Sample 3x3 area around the coordinate for better accuracy
        offset = [-1, 0, 1]
        color_samples = []

        for y_offset in offset:
            for x_offset in offset:
                y, x = coordinates[0] + y_offset, coordinates[1] + x_offset
                # Ensure coordinates are within frame bounds
                if 0 <= y < frame.shape[0] and 0 <= x < frame.shape[1]:
                    color = frame[y, x, [2, 1, 0]]  # BGR to RGB
                    color_samples.append(list(map(int, color)))

        if not color_samples:
            raise ColorDetectionError(f"No valid color samples at coordinates {coordinates}")

        # Calculate average color
        avg_color = self.get_average_values(color_samples)

        # Classify the color
        return self.classify_color_by_distance(avg_color)

    def get_average_values(self, color_array: List[List[int]]) -> List[int]:
        """Calculate average RGB values from multiple samples"""
        if not color_array:
            raise ColorDetectionError("Empty color array provided")

        red_values = [color[0] for color in color_array]
        green_values = [color[1] for color in color_array]
        blue_values = [color[2] for color in color_array]

        avg_color = [
            int(sum(red_values) / len(red_values)),
            int(sum(green_values) / len(green_values)),
            int(sum(blue_values) / len(blue_values))
        ]

        return avg_color

    def classify_color_by_distance(self, rgb_color: List[int]) -> str:
        """
        Color classification using weighted Euclidean distance to calibrated values
        """
        try:
            with open("calibrated_color_values.json", 'r') as json_file:
                calibrated_colors = json.load(json_file)["colors"]
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            raise ColorDetectionError("Calibrated color values file not found or invalid")

        min_distance = float('inf')
        best_color = None
        distances = {}

        # Calculate weighted distances for each color
        for color_name, calibrated_rgb in calibrated_colors.items():
            # Use weighted Euclidean distance for problematic color pairs
            if color_name in ["red", "orange"]:
                # Weight red channel more heavily for red/orange distinction
                weighted_distance = math.sqrt(
                    2.0 * (rgb_color[0] - calibrated_rgb[0]) ** 2 +  # Red channel weight
                    1.0 * (rgb_color[1] - calibrated_rgb[1]) ** 2 +  # Green channel weight
                    1.0 * (rgb_color[2] - calibrated_rgb[2]) ** 2  # Blue channel weight
                )
            elif color_name in ["blue", "green"]:
                # Weight blue and green channels more heavily for blue/green distinction
                weighted_distance = math.sqrt(
                    1.0 * (rgb_color[0] - calibrated_rgb[0]) ** 2 +  # Red channel weight
                    1.5 * (rgb_color[1] - calibrated_rgb[1]) ** 2 +  # Green channel weight
                    2.0 * (rgb_color[2] - calibrated_rgb[2]) ** 2  # Blue channel weight
                )
            elif color_name in ["yellow", "white"]:
                # Weight all channels equally but add special logic for yellow/white
                weighted_distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb_color, calibrated_rgb)))
            else:
                # Standard Euclidean distance for other colors
                weighted_distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb_color, calibrated_rgb)))

            distances[color_name] = weighted_distance

            if weighted_distance < min_distance:
                min_distance = weighted_distance
                best_color = color_name

        # Enhanced confidence check with specific logic for problematic pairs
        r, g, b = rgb_color

        # Find the second best match
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])
        if len(sorted_distances) >= 2:
            second_best_color, second_distance = sorted_distances[1]
            distance_diff = second_distance - min_distance

            # If distances are very close, use additional RGB analysis
            if distance_diff < 25:
                # Yellow vs White logic
                if best_color == "yellow" and second_best_color == "white":
                    # Yellow should have more color saturation, white should be more neutral
                    if abs(r - g) < 20 and abs(g - b) < 20 and abs(r - b) < 20:
                        best_color = "white"  # Very neutral = white
                    elif r > 150 and g > 150 and b < 120:
                        best_color = "yellow"  # High red/green, low blue = yellow
                elif best_color == "white" and second_best_color == "yellow":
                    # White should be more neutral, yellow should have more color
                    if abs(r - g) > 30 or abs(g - b) > 30 or abs(r - b) > 30:
                        best_color = "yellow"  # Not neutral = yellow
                    elif r < 120 and g < 120 and b < 120:
                        best_color = "white"  # All low = white

                # Blue vs Green logic
                elif best_color == "blue" and second_best_color == "green":
                    # Blue should have higher blue component
                    if b < g + 20:  # If blue isn't significantly higher than green
                        best_color = "green"
                    elif b > r + 50 and b > g + 30:
                        best_color = "blue"  # Strong blue dominance
                elif best_color == "green" and second_best_color == "blue":
                    # Green should have higher green component
                    if g < b + 20:  # If green isn't significantly higher than blue
                        best_color = "blue"
                    elif g > r + 50 and g > b + 30:
                        best_color = "green"  # Strong green dominance

                # Red vs Orange logic (existing)
                elif best_color == "red" and second_best_color == "orange":
                    if g > r * 0.7:  # If green is too high relative to red
                        best_color = "orange"
                elif best_color == "orange" and second_best_color == "red":
                    if g < r * 0.3:  # If green is too low relative to red
                        best_color = "red"

        if best_color is None:
            raise ColorDetectionError(f"Could not classify color {rgb_color}")

        return best_color

    def set_calibrated_value(self, side: str):
        """Set calibrated color values for a specific side"""
        try:
            coordinates = COORDINATES_OF_CIRCLES[side]
            frame = self.get_frame()
            color_samples = []

            for coord in coordinates:
                if isinstance(coord, str):
                    continue  # Skip center string marker
                coord = list(reversed(coord))  # Convert to (y, x)
                if 0 <= coord[0] < frame.shape[0] and 0 <= coord[1] < frame.shape[1]:
                    color = frame[coord[0], coord[1], [2, 1, 0]]
                    color_samples.append(list(map(int, color)))

            if color_samples:
                avg_color = self.get_average_values(color_samples)

                # Update calibration file
                try:
                    with open("calibrated_color_values.json", 'r') as json_file:
                        data = json.load(json_file)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = {"colors": {}}

                data["colors"][side] = avg_color

                with open("calibrated_color_values.json", 'w') as json_file:
                    json.dump(data, json_file, indent=2)

        except Exception as e:
            raise ColorDetectionError(f"Calibration failed for side {side}: {str(e)}")

    def calibrate_specific_color(self, color_name: str):
        """
        Calibrate a specific color by sampling multiple frames for better accuracy

        Args:
            color_name: Name of the color to calibrate (yellow, blue, red, green, orange, white)
        """
        try:
            # Sample multiple frames for better accuracy
            color_samples = []
            num_samples = 10

            print(f"Calibrating {color_name}... Please keep the {color_name} face steady.")

            for i in range(num_samples):
                frame = self.get_frame()

                # Find the coordinates for this color
                if color_name in ["yellow", "orange", "blue"]:
                    coordinates = COORDINATES_OF_CIRCLES[color_name]
                else:
                    coordinates = COORDINATES_OF_CIRCLES[color_name]

                # Sample from center and edge positions
                for coord in coordinates:
                    if isinstance(coord, str):
                        continue
                    coord = list(reversed(coord))
                    if 0 <= coord[0] < frame.shape[0] and 0 <= coord[1] < frame.shape[1]:
                        color = frame[coord[0], coord[1], [2, 1, 0]]
                        color_samples.append(list(map(int, color)))

                # Small delay between samples
                import time
                time.sleep(0.1)

            if color_samples:
                avg_color = self.get_average_values(color_samples)

                # Update calibration file
                try:
                    with open("calibrated_color_values.json", 'r') as json_file:
                        data = json.load(json_file)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = {"colors": {}}

                data["colors"][color_name] = avg_color

                with open("calibrated_color_values.json", 'w') as json_file:
                    json.dump(data, json_file, indent=2)

                print(f"{color_name} calibrated: RGB{avg_color}")
            else:
                print(f"No valid samples for {color_name}")

        except Exception as e:
            print(f"Calibration failed for {color_name}: {str(e)}")

    def calibrate_values(self):
        """Calibrate color values for all sides this camera handles"""
        for side in self.sides:
            self.set_calibrated_value(side)

    def release(self):
        """Release camera resources"""
        self.camera.release()


class Scanner:
    def __init__(self):
        """Initialize scanner with two cameras"""
        try:
            self.upper_camera = Camera(2, ["yellow", "orange", "blue"])
            self.lower_camera = Camera(0, ["green", "red", "white"])
        except CameraConnectionError as e:
            raise CameraConnectionError(f"Failed to initialize cameras: {str(e)}")

        self.sides = ["yellow", "red", "green", "orange", "blue", "white"]
        self.calibrated_values = {}

    def get_colors_values(self):
        """Load calibrated color values from file"""
        try:
            with open("calibrated_color_values.json", 'r') as json_file:
                data = json.load(json_file)
                self.calibrated_values = data["colors"]
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            raise ColorDetectionError("Calibrated color values file not found or invalid")

    def calibrate_values(self):
        """Calibrate both cameras"""
        self.upper_camera.calibrate_values()
        self.lower_camera.calibrate_values()

    def scan_cube(self) -> str:
        """
        Scan the entire cube and return its state as a string

        Returns:
            String representation of cube state (54 characters)
        """
        self.get_colors_values()

        # Define the order of faces in the output string - CORRECTED ORDER
        face_order = ["yellow", "blue", "red", "green", "orange", "white"]
        cube_state = ""

        # Scan each face
        for face in face_order:
            if face in ["yellow", "orange", "blue"]:
                colors = self.upper_camera.get_colors_array(face)
            else:  # green, red, white
                colors = self.lower_camera.get_colors_array(face)

            # Convert colors to single letters
            for color in colors:
                if color in COLOR_MAPPING:
                    cube_state += COLOR_MAPPING[color]
                else:
                    raise ColorDetectionError(f"Unknown color detected: {color}")

        # Validate output length
        if len(cube_state) != 54:
            raise ColorDetectionError(f"Invalid cube state length: {len(cube_state)} (expected 54)")

        return cube_state

    def get_cube_state(self, max_retries: int = 5) -> str:
        """
        Get cube state with retry mechanism

        Args:
            max_retries: Maximum number of retry attempts

        Returns:
            Valid cube state string
        """
        for attempt in range(max_retries):
            try:
                cube_state = self.scan_cube()
                # Basic validation: check if each face has correct center color
                if self.validate_cube_state(cube_state):
                    return cube_state
                else:
                    print(f"Attempt {attempt + 1}: Invalid cube state detected, retrying...")
            except (ColorDetectionError, CameraConnectionError) as e:
                print(f"Attempt {attempt + 1}: {str(e)}, retrying...")
                if attempt == max_retries - 1:
                    raise

        raise ColorDetectionError(f"Failed to get valid cube state after {max_retries} attempts")

    def validate_cube_state(self, cube_state: str) -> bool:
        """
        Basic validation of cube state

        Args:
            cube_state: 54-character string representing cube state

        Returns:
            True if state appears valid, False otherwise
        """
        if len(cube_state) != 54:
            return False

        # Check that each face has the correct center color
        # Face order: yellow, blue, red, green, orange, white
        face_centers = [4, 13, 22, 31, 40, 49]  # Center positions for each face
        expected_centers = ["y", "b", "r", "g", "o", "w"]

        for i, center_pos in enumerate(face_centers):
            if cube_state[center_pos] != expected_centers[i]:
                return False

        # Check that all colors are valid
        valid_colors = set("yrgbow")
        if not all(color in valid_colors for color in cube_state):
            return False

        return True

    def release_cameras(self):
        """Release both cameras"""
        self.upper_camera.release()
        self.lower_camera.release()


def showing_frame():
    """
    Display camera feeds for calibration and debugging.
    Always shows both cameras.
    """
    try:
        cap_1 = cv.VideoCapture(2)
        cap_2 = cv.VideoCapture(0)

        if not cap_1.isOpened():
            raise CameraConnectionError("Failed to open first camera")
        if not cap_2.isOpened():
            raise CameraConnectionError("Failed to open second camera")

        # Create camera objects to use preprocessing
        upper_cam = Camera(2, ["yellow", "orange", "blue"])
        lower_cam = Camera(0, ["green", "red", "white"])

        while True:
            # Get original frames
            ret_1, frame_1_orig = cap_1.read()
            ret_2, frame_2_orig = cap_2.read()

            if not ret_1:
                raise CameraConnectionError("Failed to read from first camera")
            if not ret_2:
                raise CameraConnectionError("Failed to read from second camera")

            # Get preprocessed frames
            frame_1_processed = upper_cam.preprocess_frame(frame_1_orig)
            frame_2_processed = lower_cam.preprocess_frame(frame_2_orig)

            # Draw calibration circles on both original and processed frames
            for i in range(9):
                # Original frames
                cv.circle(frame_2_orig, coordinates_of_circles_WHITE_[i], 5, (0, 255, 0))
                cv.circle(frame_2_orig, coordinates_of_circles_RED_[i], 5, (0, 255, 0))
                cv.circle(frame_2_orig, coordinates_of_circles_GREEN_[i], 5, (0, 255, 0))
                cv.circle(frame_1_orig, coordinates_of_circles_BLUE_[i], 5, (0, 255, 0))
                cv.circle(frame_1_orig, coordinates_of_circles_ORANGE_[i], 5, (0, 255, 0))
                cv.circle(frame_1_orig, coordinates_of_circles_YELLOW_[i], 5, (0, 255, 0))

                # Processed frames
                cv.circle(frame_2_processed, coordinates_of_circles_WHITE_[i], 5, (0, 255, 0))
                cv.circle(frame_2_processed, coordinates_of_circles_RED_[i], 5, (0, 255, 0))
                cv.circle(frame_2_processed, coordinates_of_circles_GREEN_[i], 5, (0, 255, 0))
                cv.circle(frame_1_processed, coordinates_of_circles_BLUE_[i], 5, (0, 255, 0))
                cv.circle(frame_1_processed, coordinates_of_circles_ORANGE_[i], 5, (0, 255, 0))
                cv.circle(frame_1_processed, coordinates_of_circles_YELLOW_[i], 5, (0, 255, 0))

            frame_2_orig = cv.flip(frame_2_orig, 0)
            frame_2_processed = cv.flip(frame_2_processed, 0)

            # Display both original and processed frames
            cv.imshow('Lower Camera - Original', frame_2_orig)
            cv.imshow('Lower Camera - Processed', frame_2_processed)
            cv.imshow('Upper Camera - Original', frame_1_orig)
            cv.imshow('Upper Camera - Processed', frame_1_processed)

            if cv.waitKey(1) == ord('q'):
                break

    except Exception as e:
        print(f"Error in showing_frame: {str(e)}")
    finally:
        cap_1.release()
        cap_2.release()
        cv.destroyAllWindows()


def debug_color_detection():
    """Debug function to show what colors are being detected at each position"""
    try:
        scanner = Scanner()

        # Test each face individually
        faces = ["yellow", "blue", "red", "green", "orange", "white"]

        for face in faces:
            print(f"\n=== {face.upper()} FACE ===")
            if face in ["yellow", "orange", "blue"]:
                colors = scanner.upper_camera.get_colors_array(face)
            else:
                colors = scanner.lower_camera.get_colors_array(face)

            # Print colors in 3x3 grid format
            for i in range(3):
                row = colors[i * 3:(i + 1) * 3]
                print(f"Row {i + 1}: {row}")

        scanner.release_cameras()

    except Exception as e:
        print(f"Debug error: {str(e)}")


def recalibrate_problematic_colors():
    """Recalibrate the colors that are being confused"""
    try:
        scanner = Scanner()

        # Recalibrate the problematic colors
        problematic_colors = ["yellow", "blue", "green", "white"]

        print("Recalibrating problematic colors...")
        print("Please make sure the cube is in the correct position for each color.")

        for color in problematic_colors:
            print(f"\nPreparing to calibrate {color}...")
            input(f"Press Enter when the {color} face is properly positioned and lit...")

            if color in ["yellow", "orange", "blue"]:
                scanner.upper_camera.calibrate_specific_color(color)
            else:
                scanner.lower_camera.calibrate_specific_color(color)

        print("\nRecalibration complete!")
        scanner.release_cameras()

    except Exception as e:
        print(f"Recalibration error: {str(e)}")


# Example usage
if __name__ == "__main__":
    # For calibration and debugging
    # showing_frame()

    # For debugging color detection
    # debug_color_detection()

    # For actual scanning
    try:
        scanner = Scanner()
        # scanner.calibrate_values()
        cube_state = scanner.get_cube_state()
        print(f"Cube state: {cube_state}")
        scanner.release_cameras()
    except Exception as e:
        print(f"Error: {str(e)}")
