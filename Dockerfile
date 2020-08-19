FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/carservice

COPY ./requirements.txt usr/src/carservice/requirements.txt
RUN pip install -r usr/src/carservice/requirements.txt

COPY . /usr/src/carservice

EXPOSE 8000
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]