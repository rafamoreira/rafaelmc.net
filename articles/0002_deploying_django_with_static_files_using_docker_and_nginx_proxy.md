--- 
title: Deploying Django app with static files using Docker and Nginx proxy 
date: 2023-08-01
---

This task is more complicated than I first thought it would be. 
For someone accustomed to Docker and all its intricacies, it probably wouldn't 
be so much, but here we are.
Before anything, here are the two main docker-compose files used to achieve this 
setup; and this setup is what is being used to serve this website as of now.

first is the acme/nginx-proxy
Here a example of the docker-compose for the proxy:

```yaml
# docker-compose-nginx-proxy.yml 
---
services:
  nginx-proxy:
    image: nginxproxy/nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro
      - /root/docker/nginx/htpasswd:/etc/nginx/htpasswd
      - /root/docker/nginx/certs:/etc/nginx/certs
      - /root/docker/nginx/vhost:/etc/nginx/vhost.d
      - /root/docker/nginx/html:/usr/share/nginx/html
    networks:
      - proxy
  nginx-proxy-acme:
    image: nginxproxy/acme-companion
    volumes_from:
      - nginx-proxy
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /root/docker/nginx/acme:/etc/acme.sh
    environment:
      - DEFAULT_EMAIL=me@rafaelmc.net
    networks:
      - proxy
networks:
  proxy:
```

The second one is the one taking care of django, and serving the static files.

```yaml
# docker-compose.yaml
---
version: "3"

services:
  web:
    image: rfmc28/rafaelmc.net:latest
    command: bash -c "python manage.py migrate && python manage.py collectstatic --no-input && gunicorn rafaelmc.wsgi -b 0.0.0.0:8000"
    container_name: rafaelmc
    volumes:
      - sqlite_data:/app/sqlite_data/
      - /root/sqlite_backups/:/sqlite_backups/
      - /root/docker/envfiles/rafaelmc.net.env:/app/.env
      - static_files:/app/static/
    expose:
      - "8000"
    environment:
      - VIRTUAL_HOST=rafaelmc.net # www.rafaelmc.net
      - VIRTUAL_PORT=8000
      - LETSENCRYPT_HOST=rafaelmc.net # www.rafaelmc.net
      - VIRTUAL_PATH=/
      # - VIRTUAL_DEST=/static
    networks:
      - proxy

  static:
    image: nginx
    expose:
      - "80"
    environment:
      - VIRTUAL_HOST=rafaelmc.net #,www.rafaelmc.net
      - VIRTUAL_PORT=80
      # - LETSENCRYPT_HOST=rafaelmc.net #,www.rafaelmc.net
      - VIRTUAL_PATH=/static/
      - VIRTUAL_DEST=/
    volumes:
      - static_files:/usr/share/nginx/html/
    networks:
      - proxy
    depends_on:
      - web
networks:
  proxy:
    name: nginx-proxy_proxy
volumes:
  sqlite_data:
  static_files:
```

I think it's better to already lay out all the files, and go on a little more 
detail on whys, and hows.

I think the first thing to note is that I'm separating this into two different 
docker-compose files because I'm running those on Portainer, so each compose 
file will be it's own `stack`.
Portainer is entirely optional for the task, and it's possible and easy to 
combine those two compose files into one.

The most critical—and challenging to decipher from the documentation—are the 
`VIRTUAL_PATH` and `VIRTUAL_DEST` variables defined on the django compose. 
Although these variables are documented on the `nginx-proxy` image, 
understanding their meaning can be tricky if you're not familiar with Docker and 
Nginx terminology, at least it was for me.

Let's examine the web container, which is designed to serve the entire website, 
except for everything that resides in /static. The `VIRTUAL_PATH` for the web is 
`/`, meaning it serves everything. If you don't split your Nginx proxy into 
multiple containers you will never need to set this, and everything will operate 
as expected.

Next, we have the static container—a basic Nginx container. This one contains 
both `VIRTUAL_PATH` and `VIRTUAL_DEST` env variables. Here, `VIRTUAL_PATH` is 
equivalent to defining a location `/static` in `nginx.conf`.

While nginx can smartly interpret `//` as the root, it might be confusing for 
those like myself. To clear this up, I've defined `VIRTUAL_DEST=/`, which means 
nginx will receive the requests on the path relative as if they were on the root 
`/`.

For instance, let's say we have a file, example.com/static/css/style.css, and 
this is the complete path. This file will be routed to the static container, as 
it's part of `/static/`. Upon reaching the static container, the request appears 
as if it were on `root/css/style.css`.

The final point to note is the structure of the `static_files` volume. A 
`static_files` volume is declared and used by both the static nginx and web 
containers. When we mount the volume, it will initially be empty. 

However, with the command defined on the web container - 
`python admin.py collectstatic --no-input` - it copies the necessary files there. 
Consequently, all the static files will become accessible to both containers, 
the downside is that to be able to achieve some sort of automation, you need to 
run `collecstatic` for every deployment, even if you didn't change anything. It 
shouldn't be a problem, for this simple website it's very fast on my local 
machine:


```bash
(.venv)rmc@mercury.local ~/code/python/rafaelmc % time ./manage.py collectstatic --no-input                                                             [master|…1]

0 static files copied to '/Users/rmc/code/python/rafaelmc/staticfiles', 132 unmodified.
./manage.py collectstatic --no-input  0.14s user 0.04s system 95% cpu 0.186 total
(.venv)rmc@mercury.local ~/code/python/rafaelmc %
```


Take a look on the [repository](https://git.sr.ht/~rafaelmc/rafaelmc.net.git)
