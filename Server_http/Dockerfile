FROM python:3.10-alpine
RUN mkdir templates
ADD server.py requirements.txt .
ADD templates ./templates
RUN pip install -r requirements.txt
CMD ["python","./server.py"]