FROM python:3.7
RUN pip install pipenv
COPY . .
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8050
CMD python3 run app.py 