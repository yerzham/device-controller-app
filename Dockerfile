FROM python:3-alpine

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install waitress

COPY . .
RUN pip install -e .
CMD [ "waitress-serve", "--port=5050", "--call", "flaskr:create_app" ]