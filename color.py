class Color:
    def __init__(self, name: str, letter: str, hex_code: str) -> None:
        self.name = name
        self.letter = letter
        self.hex_code = hex_code

    def __repr__(self) -> str:
        return self.letter
