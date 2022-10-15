FROM node:lts
RUN mkdir -p /app
WORKDIR /app

COPY ./package*.json /app/

RUN npm install
RUN npm install -g @angular/cli

EXPOSE 4200 49153