FROM python

WORKDIR /MessageBroker

COPY . .

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "MessageBroker.py"]

EXPOSE 4000
EXPOSE 5000/udp
EXPOSE 5976