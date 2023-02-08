FROM python:3.8.3-alpine

WORKDIR /the/workdir/path

COPY requirements.txt ./

COPY code.py ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./code.py"]