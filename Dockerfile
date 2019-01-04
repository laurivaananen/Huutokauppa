from python:3.6

RUN mkdir huutokauppa

WORKDIR huutokauppa/

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./run.py .

COPY ./application application

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8001", "application:application"]