FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-binary :all: --only-binary pandas -r requirements.txt

COPY . .

CMD ["python", "budget_bot.py"]
