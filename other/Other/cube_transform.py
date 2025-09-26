from typing import List


SOLVED_STATE = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"


def _rotate_face_cw(state: List[str], idxs: List[int]):
    a, b, c, d, e, f, g, h, i = [state[k] for k in idxs]
    # rotate clockwise
    rotated = [g, d, a, h, e, b, i, f, c]
    for pos, val in zip(idxs, rotated):
        state[pos] = val


def _move_U(state: List[str]):
    u = list(range(0, 9))
    l = list(range(9, 18))
    f = list(range(18, 27))
    r = list(range(27, 36))
    b = list(range(36, 45))
    _rotate_face_cw(state, u)
    tmp = [state[f[0]], state[f[1]], state[f[2]]]
    state[f[0]], state[f[1]], state[f[2]] = state[l[0]], state[l[1]], state[l[2]]
    state[l[0]], state[l[1]], state[l[2]] = state[b[0]], state[b[1]], state[b[2]]
    state[b[0]], state[b[1]], state[b[2]] = state[r[0]], state[r[1]], state[r[2]]
    state[r[0]], state[r[1]], state[r[2]] = tmp


def _move_D(state: List[str]):
    l = list(range(9, 18))
    f = list(range(18, 27))
    r = list(range(27, 36))
    b = list(range(36, 45))
    d = list(range(45, 54))
    _rotate_face_cw(state, d)
    tmp = [state[f[6]], state[f[7]], state[f[8]]]
    state[f[6]], state[f[7]], state[f[8]] = state[r[6]], state[r[7]], state[r[8]]
    state[r[6]], state[r[7]], state[r[8]] = state[b[6]], state[b[7]], state[b[8]]
    state[b[6]], state[b[7]], state[b[8]] = state[l[6]], state[l[7]], state[l[8]]
    state[l[6]], state[l[7]], state[l[8]] = tmp


def _move_F(state: List[str]):
    u = list(range(0, 9))
    l = list(range(9, 18))
    f = list(range(18, 27))
    r = list(range(27, 36))
    d = list(range(45, 54))
    _rotate_face_cw(state, f)
    tmp = [state[u[6]], state[u[7]], state[u[8]]]
    state[u[6]], state[u[7]], state[u[8]] = state[l[8]], state[l[5]], state[l[2]]
    state[l[8]], state[l[5]], state[l[2]] = state[d[2]], state[d[1]], state[d[0]]
    state[d[2]], state[d[1]], state[d[0]] = state[r[0]], state[r[3]], state[r[6]]
    state[r[0]], state[r[3]], state[r[6]] = tmp


def _move_B(state: List[str]):
    u = list(range(0, 9))
    r = list(range(27, 36))
    b = list(range(36, 45))
    l = list(range(9, 18))
    d = list(range(45, 54))
    _rotate_face_cw(state, b)
    tmp = [state[u[0]], state[u[1]], state[u[2]]]
    state[u[0]], state[u[1]], state[u[2]] = state[r[2]], state[r[5]], state[r[8]]
    state[r[2]], state[r[5]], state[r[8]] = state[d[8]], state[d[7]], state[d[6]]
    state[d[8]], state[d[7]], state[d[6]] = state[l[6]], state[l[3]], state[l[0]]
    state[l[6]], state[l[3]], state[l[0]] = tmp


def _move_R(state: List[str]):
    u = list(range(0, 9))
    f = list(range(18, 27))
    r = list(range(27, 36))
    b = list(range(36, 45))
    d = list(range(45, 54))
    _rotate_face_cw(state, r)
    tmp = [state[u[2]], state[u[5]], state[u[8]]]
    state[u[2]], state[u[5]], state[u[8]] = state[f[2]], state[f[5]], state[f[8]]
    state[f[2]], state[f[5]], state[f[8]] = state[d[2]], state[d[5]], state[d[8]]
    state[d[2]], state[d[5]], state[d[8]] = state[b[6]], state[b[3]], state[b[0]]
    state[b[6]], state[b[3]], state[b[0]] = tmp


def _move_L(state: List[str]):
    u = list(range(0, 9))
    l = list(range(9, 18))
    f = list(range(18, 27))
    b = list(range(36, 45))
    d = list(range(45, 54))
    _rotate_face_cw(state, l)
    tmp = [state[u[0]], state[u[3]], state[u[6]]]
    state[u[0]], state[u[3]], state[u[6]] = state[b[8]], state[b[5]], state[b[2]]
    state[b[8]], state[b[5]], state[b[2]] = state[d[6]], state[d[3]], state[d[0]]
    state[d[6]], state[d[3]], state[d[0]] = state[f[0]], state[f[3]], state[f[6]]
    state[f[0]], state[f[3]], state[f[6]] = tmp


def _apply_basic(state: List[str], face: str):
    if face == 'U':
        _move_U(state)
    elif face == 'D':
        _move_D(state)
    elif face == 'F':
        _move_F(state)
    elif face == 'B':
        _move_B(state)
    elif face == 'R':
        _move_R(state)
    elif face == 'L':
        _move_L(state)
    else:
        raise ValueError(f"Unknown face: {face}")


def _expand_token(token: str) -> List[str]:
    """Expand a token like "U2" or "UD'" into a list of single-face moves.
    Example: "UD'" -> ["U", "D'"]
    """
    moves: List[str] = []
    i = 0
    while i < len(token):
        face = token[i]
        i += 1
        mod = ''
        if i < len(token) and token[i] in ("'", '2'):
            mod = token[i]
            i += 1
        moves.append(face + mod)
    return moves


def expand_moves(tokens: List[str]) -> List[str]:
    expanded: List[str] = []
    for tk in tokens:
        expanded.extend(_expand_token(tk))
    return expanded


def apply_moves_to_state(tokens: List[str], start_state: str = SOLVED_STATE) -> str:
    state = list(start_state)
    for move in tokens:
        face = move[0]
        modifier = move[1:] if len(move) > 1 else ''
        if modifier == "":
            _apply_basic(state, face)
        elif modifier == "'":
            # counterclockwise = 3 times clockwise
            _apply_basic(state, face)
            _apply_basic(state, face)
            _apply_basic(state, face)
        elif modifier == '2':
            _apply_basic(state, face)
            _apply_basic(state, face)
        else:
            raise ValueError(f"Unknown modifier in move: {move}")
    return ''.join(state)


