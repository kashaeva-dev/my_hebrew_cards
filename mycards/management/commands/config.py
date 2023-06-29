logger_config = {
    'version': 1,
    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': '{',
            },
        },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'std_format',
            'level': 'INFO',
            },
        },
    'loggers': {
        'bot_logger': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}