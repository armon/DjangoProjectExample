server {
    listen 81;
    server_name .example.com;
    set $home /server/env.example.com;

    client_max_body_size 10m;
    keepalive_timeout 120;

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_redirect http://127.0.0.1:8000/ http://localhost:7000/;
    }

    location /media/ {
        root $home/project/public;
        autoindex on;
    }
}
