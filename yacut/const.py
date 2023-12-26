from string import ascii_letters, digits


PATTERN_FOR_SHORT = ascii_letters + digits
PATTERN = rf"^[{PATTERN_FOR_SHORT}]+$"
LEN_OF_SHORT = 6
ORIGINAL_LENGTH = 3000
SHORT_LENGTH = 16
REDIRECT_VIEW = 'redirect_view'
