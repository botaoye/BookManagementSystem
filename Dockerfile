FROM python:3.6-alpine

RUN adduser -D bookmanage

WORKDIR /home/bookmanage

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN venv/bin/pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY app app
COPY bookManagementSystem.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP bookManagementSystem.py

RUN chown -R bookmanage:bookmanage ./
USER bookmanage

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]