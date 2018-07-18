FROM python:3.6.5
COPY .env README.MD fruits.csv requirements.txt Masky.py test_class.py /Masky/
WORKDIR /Masky
RUN pip install -r requirements.txt
