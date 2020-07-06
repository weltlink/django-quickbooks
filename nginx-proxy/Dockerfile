FROM nginx:1.18.0

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf.template /etc/nginx/nginx.conf.template

COPY run_nginx /run_nginx

RUN chmod +x /run_nginx

CMD /run_nginx
