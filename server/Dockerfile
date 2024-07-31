FROM python:alpine
WORKDIR /Users/markprosser/Code/bettermint/server
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_APP=/Users/markprosser/Code/bettermint/server/app.py
CMD ["flask", "run", "--host", "0.0.0.0"]