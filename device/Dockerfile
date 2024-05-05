FROM python

WORKDIR /device

COPY . .

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "device.py"]