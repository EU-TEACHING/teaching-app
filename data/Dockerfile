ARG ARCH
FROM chronis10/teaching-base:${ARCH}
WORKDIR /app
COPY /influxdb /app/influxdb
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt
CMD ["python3", "main.py"]