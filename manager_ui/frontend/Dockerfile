FROM nginx:1.25-alpine

COPY manager_ui/frontend /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
