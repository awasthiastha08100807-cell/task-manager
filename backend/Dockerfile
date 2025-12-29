FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make wait-for-it.sh executable
RUN chmod +x wait-for-it.sh

# Install netcat for wait-for-it.sh
RUN apt-get update && apt-get install -y netcat-openbsd

CMD ["./wait-for-it.sh", "mysql:3306", "--", "python", "app.py"]
