FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
<<<<<<< HEAD
CMD ["python", "subtitle.py"]
=======
CMD ["python", "subtitle.py"]
>>>>>>> 68fdd92a08c4f5783f8ef6327e743205ad3fda3c
