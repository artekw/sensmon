FROM hypriot/rpi-alpine-scratch
MAINTAINER Artur Wronowski "arteqw@gmail.com"
RUN apk add --update python py-pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["sensmon.py"]