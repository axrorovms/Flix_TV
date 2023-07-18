FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY compose/nginx/nginx.conf_1 /etc/nginx/conf.d
COPY compose/nginx/nginx.conf /etc/nginx/nginx.conf
