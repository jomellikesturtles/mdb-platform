FROM nginx:alpine

# Copy the built application from local dist to nginx html directory
COPY . /usr/share/nginx/html

# Copy custom nginx configuration to handle SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]
