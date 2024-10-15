import logging


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[34m',  # Blue
        'INFO': '\033[1;37m',  # Bright White
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[31m',  # Red
        'TIME': '\033[32m',  # Green for time
    }

    def __init__(self, show_time=True, show_date=True):
        super().__init__()
        self.show_time = show_time
        self.show_date = show_date

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        message = super().format(record)

        badge = f"{log_color}|  {record.levelname}  |"
        formatted_message = f"{badge} {log_color}{message}"

        if self.show_time and self.show_date:
            formatted_message = f"{self.COLORS['TIME']}{self.formatTime(record)} {formatted_message}"
        elif self.show_time:
            formatted_time = self.formatTime(record, datefmt='%H:%M:%S')
            milliseconds = f"{int(record.msecs // 100)}"
            formatted_message = f"{self.COLORS['TIME']}{formatted_time}.{milliseconds} {formatted_message}"
        elif self.show_date:
            formatted_message = f"{self.COLORS['TIME']}{self.formatTime(record, datefmt='%Y-%m-%d')} {formatted_message}"

        return formatted_message
