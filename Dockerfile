FROM  python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
<<<<<<< HEAD
RUN python -m pip install -r requirements.txt 
=======
RUN pip install -r requirements.txt 
>>>>>>> origin/main

# Copy project
COPY . /code/