# from .celery import app
import pymysql
pymysql.install_as_MySQLdb()

from .celery import app as spug

__all__ = ('spug')

