FROM python:3.14-slim-trixie

RUN apt update && apt install -y postgresql-client-17

COPY elt_script.py .

CMD ["python", "elt_script.py"]
