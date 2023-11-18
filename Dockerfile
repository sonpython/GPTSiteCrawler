# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Define environment variable for non-interactive mode
ENV PYTHONUNBUFFERED 1

# Expose the port the app runs on
EXPOSE 8080

# Run crawl.py when the container launches
CMD ["sh", "-c", "echo ${CRAWLER_URL}"]
CMD ["sh", "-c", "echo ${CRAWLER_SELECTOR}"]
CMD ["sh", "-c", "echo ${CRAWLER_CHUNK_SIZE}"]
CMD ["sh", "-c", "echo ${CRAWLER_MAX_LINKS}"]
CMD ["sh", "-c", "python /app/src/main.py ${CRAWLER_URL} --selectors ${CRAWLER_SELECTOR} --annotate-size ${CRAWLER_CHUNK_SIZE} --max-links ${CRAWLER_MAX_LINKS}}"]