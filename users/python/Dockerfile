FROM python:3.7.7-slim


COPY * /opt/microservices/
COPY requirements.txt /opt/microservices/

RUN pip install --upgrade pip \
  && pip install --upgrade pipenv\
  && apt-get clean \
  && apt-get update \
  && apt install -y build-essential \
  && pip install --upgrade -r /opt/microservices/requirements.txt

USER 1001

EXPOSE 8081
WORKDIR /opt/microservices/

CMD ["python", "users.py", "8081"]
