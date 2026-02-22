# Stage 1: Serve the application with Nginx
FROM nginx:stable-alpine

# Copy the pre-built output to Nginx's html directory
COPY dist/mdb-electron /usr/share/nginx/html

# Copy a custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
