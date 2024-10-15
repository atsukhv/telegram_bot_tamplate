import logging

class ColoredFormatter(logging.Formatter):
    # ANSI escape sequences for colors
    COLORS = {
        'DEBUG': '\033[34m',  # Blue
        'INFO': '\033[37m',   # White
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',   # Red
        'CRITICAL': '\033[37m\033[41m',  # White text on Red background
        'SUCCESS': '\033[32m',  # Green
        'RESET': '\033[0m',     # Reset to default
        'TIME': '\033[32m',     # Green for time
    }

    def __init__(self, show_time=True, show_date=True):
        super().__init__()
        self.show_time = show_time
        self.show_date = show_date

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        message = super().format(record)

        # Форматирование шильдика
        badge = f"|  {record.levelname}  |"
        formatted_message = f"{log_color}{badge} {message}{self.COLORS['RESET']}"

        # Добавление времени и даты в зависимости от настроек
        if self.show_time and self.show_date:
            formatted_message = f"{self.COLORS['TIME']}{self.formatTime(record)} {formatted_message}"
        elif self.show_time:
            # Форматируем время с секундами и миллисекундами
            formatted_time = self.formatTime(record, datefmt='%H:%M:%S')
            milliseconds = f"{int(record.msecs):03d}"  # Получаем миллисекунды
            formatted_message = f"{self.COLORS['TIME']}{formatted_time}.{milliseconds} {formatted_message}"
        elif self.show_date:
            formatted_message = f"{self.COLORS['TIME']}{self.formatTime(record, datefmt='%Y-%m-%d')} {formatted_message}"

        return formatted_message
