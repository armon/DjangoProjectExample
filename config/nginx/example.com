server {
    listen 80;
    server_name .example.com;
    set $home /server/env.example.com;

    client_max_body_size 10m;
    keepalive_timeout 120;

    location / {
        uwsgi_pass uwsgi_main;
        include uwsgi_params;
        uwsgi_param SCRIPT_NAME "";
        uwsgi_param UWSGI_CHDIR $home/project;
        uwsgi_param UWSGI_SCRIPT wsgi;
        uwsgi_param UWSGI_PYHOME $home;
    }

    location /media/ {
        root $home/project/public;
        autoindex on;
        expires 1h;
    }
}
