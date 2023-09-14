class Color:
    def __init__(self, name: str, letter: str, hex_code: str) -> None:
        """
        This function initializes an object of the Color class.
        :param name:
        :param letter:
        :param hex_code:
        """
        self.name = name
        self.letter = letter
        self.hex_code = hex_code

    def __repr__(self) -> str:
        """
        This function defines how a Color object is represented when printed.
        :return:
        """
        return self.letter

    def __str__(self) -> str:
        """
        This function defines how a Color object is turned into a str object.
        :return:
        """
        return self.letter
