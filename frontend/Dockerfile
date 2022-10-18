FROM node:lts
RUN mkdir -p /app
WORKDIR /app

COPY ./package*.json /app/

RUN npm install --global --force yarn
RUN yarn global add @angular/cli
RUN yarn global add tailwindcss postcss autoprefixer
RUN ng config -g cli.packageManager yarn


EXPOSE 4200 49153