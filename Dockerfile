FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/
EXPOSE 5000
ENV FLASK_APP=src/app.py
CMD ["python", "src/app.py"]
# Docker configurado para chatbot Flask
