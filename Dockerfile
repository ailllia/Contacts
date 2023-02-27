FROM python:3.11-alpine
WORKDIR /Telefonbuch
RUN pip install Flask
ENV FLASK_APP main_api.py
COPY . .
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]
