#FROM hypriot/rpi-alpine-scratch
FROM frolvlad/alpine-python3
MAINTAINER Artur Wronowski "arteqw@gmail.com"
RUN apk add --update alpine-sdk python3-dev
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
