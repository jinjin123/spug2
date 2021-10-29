DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1']
SECRET_KEY = 'I5J#.Ma9%#ka4AKw5%CMaN1@9k7XOjmb40FB.LEFJHXS983!wK'

DATABASES = {
    'default': {
        'ATOMIC_REQUESTS': True,
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spug',
        'USER': 'spug',
        'PASSWORD': 'spug.dev',
        'HOST': '127.0.0.1',
        # 'HOST': '192.168.1.107',
        'PORT': '3306',
        # 'OPTIONS': {
        #     'unix_socket': '/var/lib/mysql/mysql.sock',
            # 'charset': 'utf8mb4',
            # 'sql_mode': 'STRICT_TRANS_TABLES',
        # }
    }
}
