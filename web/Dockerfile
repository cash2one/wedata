FROM node:6

ENV NGINX_VERSION 1.9.11-1~jessie

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
  && echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
  && apt-get update \
  && apt-get install -y ca-certificates nginx=${NGINX_VERSION} gettext-base git libpng-dev bzip2 \
  && rm -rf /var/lib/apt/lists/* \
  && ln -sf /dev/stdout /var/log/nginx/access.log \
  && ln -sf /dev/stderr /var/log/nginx/error.log

WORKDIR /usr/src/app
COPY package.json /usr/src/app/
RUN yarn install

COPY . /usr/src/app
RUN yarn run build

COPY nginx.conf /etc/nginx/nginx.conf

RUN cp -r ./dist/* /usr/share/nginx/html/

CMD nginx -g 'daemon off;'
