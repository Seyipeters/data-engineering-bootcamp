#Base Image
FROM python:3.9.1

#Set working directory
WORKDIR /app

#Copy project files into the container
COPY . /app

#Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

#Default command
CMD ["python", "scripts/extract.py"]
