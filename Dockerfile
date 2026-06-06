# Use an official Python runtime as the base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import nltk; nltk.download('wordnet', download_dir='/usr/local/share/nltk_data'); nltk.download('vader_lexicon', download_dir='/usr/local/share/nltk_data')"
COPY main.py .

# Expose the port FastAPI will run on
EXPOSE 8000

# Default command (production-like; we'll override for dev with --reload)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]