from string import ascii_letters, digits

PATTERN = r'^[a-zA-Z\d]{1,16}$'
LABELS = {
    'original': 'url',
    'short': 'custom_id',
}
LEN_OF_SHORT_ID = 6
REDIRECT_VIEW = 'redirect_view'
PATTERN_FOR_GEN_URL = ascii_letters + digits
ORIGINAL_LENGTH = 256
SHORT_LENGTH = 16
REGEX_MSG = 'Используйте буквы латинского алфавита и цифры'
UNIQUE_SHORT_MSG = 'Предложенный вариант короткой ссылки уже существует.'
INDEX = 'index.html'
