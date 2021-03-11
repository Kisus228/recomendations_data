import logging
import os


log = logging.getLogger("app")
log.setLevel(os.environ.get("LOG_LEVEL", "DEBUG"))

f = logging.Formatter(
    "[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s", datefmt='%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(os.environ.get("LOG_LEVEL", "DEBUG"))
ch.setFormatter(f)
log.addHandler(ch)


class Config:
    HOST = os.environ.get('HOST') or 'localhost'  # env.str('HOST')
    PORT = os.environ.get('PORT') or 8080  # env.int('PORT')
    AUTHENTICATION_TOKEN_EXECMODEL = os.environ.get(
        'AUTHENTICATION_TOKEN_EXECMODEL') or '4CE7B412-49B7-3DCF-B56D-3441B6A3698A'
    # токен доступа к методу для быстрой проверки микросервиса
    AUTHENTICATION_TOKEN_PINGMODEL = os.environ.get(
        'AUTHENTICATION_TOKEN_PINGMODEL') or '2227E485-B53C-2A52-80CA-230BE296AAB1'
    API_URL = os.environ.get('API_URL') or 'https://test.ru/'
    REQUEST_PATH = os.environ.get('REQUEST_PATH') or 'api/v1/subject_features/'  # :subject
    BEARER_TOKEN = os.environ.get('BEARER_TOKEN') or 'abcdef123'


config = Config()
