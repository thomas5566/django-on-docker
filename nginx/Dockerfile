FROM nginx:1.19.0-alpine

# By default, Nginx looks in the /usr/share/nginx/html directory
# inside of the container for files to serve
RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

# 关闭守护模式
CMD ["nginx", "-g", "daemon off;"]