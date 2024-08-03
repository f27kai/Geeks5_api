FROM python:3.12
ENV PYTHONWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY . /app/