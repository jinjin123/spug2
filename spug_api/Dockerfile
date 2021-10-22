FROM registry.aliyuncs.com/openspug/spug
ADD spug.ini /etc/supervisord.d/spug.ini
RUN python3 -m pip install celery==5.1.2  
RUN python3 -m pip install django-celery-beat==2.2.1 
RUN python3 -m pip install django-celery-results==2.2.0
RUN python3 -m pip install pymysql
RUN python3 -m pip install django-mysql==4.0.0
RUN python3 -m pip install xlrd
RUN python3 -m pip install xlwt
RUN python3 -m pip install ansible==2.9.6
RUN python3 -m pip install ansible_runner
RUN python3 -m pip install ansible_inventory
RUN python3 -m pip install rsa
RUN sed -i 's/query.decode/query.encode/g' /usr/local/lib/python3.6/site-packages/django/db/backends/mysql/operations.py

