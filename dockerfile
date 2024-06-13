FROM python:3.10.6

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY project project
COPY setup.py setup.py
RUN pip install .


CMD uvicorn project.app.conta_app:app --host 0.0.0.0 --port $PORT