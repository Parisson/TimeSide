FROM node:15

WORKDIR /srv/app/

EXPOSE 8000

COPY . /srv/app

RUN chown node -R /srv/app

USER node

CMD [ "yarn", "run", "install:build:prod" ]