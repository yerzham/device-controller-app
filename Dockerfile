FROM python:3-alpine
RUN pip install --upgrade pip
RUN pip install waitress
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "waitress-serve", "--port=5050", "--call", "flaskr:create_app" ]