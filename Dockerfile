FROM python:3.9

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python generate_data.py

EXPOSE 5000

CMD ["python", "main.py"]