from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QApplication,
)
from PySide6.QtGui import QIcon

from other.Other.cube_transform import apply_moves_to_state, expand_moves


class CubeViewerWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Просмотр состояния кубика")
        self.setWindowIcon(QIcon("images/logo/cubing_robot_logo_icon.png"))

        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout(self.central)

        # Create 6 faces as 3x3 label grids laid out in a net
        self.face_grids = []
        self.labels = []  # flat 54 labels in order y b r g o w

        # Net layout using a grid
        net = QGridLayout()
        net.setHorizontalSpacing(8)
        net.setVerticalSpacing(8)

        def create_face() -> list[list[QLabel]]:
            face = []
            for _ in range(3):
                row = []
                for _ in range(3):
                    lab = QLabel(" ")
                    lab.setFixedSize(32, 32)
                    lab.setStyleSheet("background: #222; border: 1px solid #333;")
                    lab.setScaledContents(True)
                    row.append(lab)
                face.append(row)
            return face

        # Build faces
        faces = [create_face() for _ in range(6)]
        # Arrange as:   U
        #            L  F  R  B
        #               D
        # Our state order is: Y B R G O W -> map to U L F R B D by color names
        # We'll place: U at (0,3), L at (1,2), F at (1,3), R at (1,4), B at (1,5), D at (2,3)
        positions = [(0, 3), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3)]
        for idx, (row, col) in enumerate(positions):
            for r in range(3):
                for c in range(3):
                    net.addWidget(faces[idx][r][c], row * 3 + r, col * 3 + c)
        self.layout.addLayout(net)

        # Scramble text and actions
        self.scramble_label = QLabel("")
        self.scramble_label.setWordWrap(True)
        self.scramble_label.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.scramble_label)

        actions = QHBoxLayout()
        self.copy_button = QPushButton("Копировать состояние")
        self.close_button = QPushButton("Закрыть")
        actions.addWidget(self.copy_button)
        actions.addWidget(self.close_button)
        self.layout.addLayout(actions)

        self.copy_button.clicked.connect(self.__copy_state__)
        self.close_button.clicked.connect(self.close)

        # Flatten labels in the same order as faces created: U, L, F, R, B, D
        for face in faces:
            for r in range(3):
                for c in range(3):
                    self.labels.append(face[r][c])

        self.color_map = {
            'y': '#ffff00',
            'b': '#0000ff',
            'r': '#ff0000',
            'g': '#008000',
            'o': '#ffa500',
            'w': '#ffffff',
        }

    def show_scramble(self, tokens: list[str]):
        expanded = expand_moves(tokens)
        state = apply_moves_to_state(expanded)
        self._last_state = state
        self._last_tokens = tokens
        self.scramble_label.setText("Скрамбл: " + " ".join(tokens))
        # State is order y b r g o w; map to visual order U, L, F, R, B, D
        # Colors: y=U, b=L, r=F, g=R, o=B, w=D
        faces = [state[0:9], state[9:18], state[18:27], state[27:36], state[36:45], state[45:54]]
        # Reorder indices to U,L,F,R,B,D by mapping [0,1,2,3,4,5] -> [0,1,2,3,4,5] with color meanings
        ordered = [faces[0], faces[1], faces[2], faces[3], faces[4], faces[5]]
        i = 0
        for face in ordered:
            for ch in face:
                self.labels[i].setStyleSheet(f"background: {self.color_map.get(ch, '#222')}; border: 1px solid black;")
                i += 1
        self.show()

    def __copy_state__(self):
        try:
            state = getattr(self, "_last_state", None)
            if state:
                QApplication.clipboard().setText(state)
        except Exception:
            pass


