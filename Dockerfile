FROM python:3-alpine3.15
WORKDIR /app
COPY . /app/
RUN pip install flask pandas
EXPOSE 3000
CMD ["python","-u","api.py"]