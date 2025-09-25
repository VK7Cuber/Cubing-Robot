from typing import List, Tuple, Optional

# Reuse the canonical encoding and parsing from Arduino connection
from Devices.Arduino.arduino_connection import find_turn_index


def normalize_scramble_text(text: str) -> str:
    """Trim, uppercase and collapse whitespace for stable parsing."""
    return " ".join(text.strip().upper().split())


def tokenize_scramble(text: str) -> List[str]:
    """Split a scramble string into move tokens by spaces after normalization."""
    normalized = normalize_scramble_text(text)
    if not normalized:
        return []
    return [token for token in normalized.split(" ") if token]


def validate_scramble(text: str) -> Tuple[bool, Optional[str], List[str]]:
    """Validate a scramble string against the robot's supported encoding.

    Returns (is_valid, error_message, tokens). If valid, error_message is None and
    tokens is the parsed list of moves. If invalid, error_message explains the first
    encountered problem and tokens may be partially parsed.
    """
    tokens = tokenize_scramble(text)
    if not tokens:
        return False, "Пустой скрамбл — введите ходы через пробел.", []

    for idx, token in enumerate(tokens, start=1):
        try:
            # This validates both single and dual-face moves using project logic
            find_turn_index(token)
        except Exception:
            return (
                False,
                f"Недопустимый ход на позиции {idx}: '{token}'. Разрешены только буквы U, D, L, F, R, B с модификаторами ' и 2, а также их допустимые пары.",
                tokens,
            )

    return True, None, tokens


def validate_multiple(scrambles: List[str]) -> List[Tuple[bool, Optional[str], List[str]]]:
    """Validate multiple scramble strings at once."""
    return [validate_scramble(s) for s in scrambles]


