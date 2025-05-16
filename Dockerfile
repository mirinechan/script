FROM python:3.12-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Set workdir
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "ytd:app", "--host", "0.0.0.0", "--port", "8000"]
