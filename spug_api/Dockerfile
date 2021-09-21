FROM registry.aliyuncs.com/openspug/spug
ADD spug.ini /etc/supervisord.d/spug.ini
RUN python3 -m pip install celery==5.1.2  
RUN python3 -m pip install django-celery-beat==2.2.1 
RUN python3 -m pip install django-celery-results==2.2.0
RUN python3 -m pip install pymysql
RUN python3 -m pip install django-mysql==4.0.0

