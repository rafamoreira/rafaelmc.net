--- 
title: Kamal v2 is awesome
date: 2024-10-08
---

A bit more than one year ago I wrote this post [# Deploying Django app with static files using Docker and Nginx proxy](https://rafaelmc.net/blog/post/0002_deploying_django_with_static_files_using_docker_and_nginx_proxy) and my opening line was:

> This task is more complicated than I first thought it would be. 

And it really was. I even dreaded putting more services on the website that would depend on that flimsy setup, but I was reading about Rails 8, and then I read that [Kamal](https://kamal-deploy.org/) would have a new version as well, so I went to take a look at it. 

When first announced, Kamal, which at that time was called MSRK, enticed me, but one limitation, which was the possibility to run only a single "service" on a server, was a deal breaker for me. My understanding was that this limitation was related to Traefik, and how that is set up, but I'm not sure about the details. I'm not even sure if that was a real limitation, or if there were workarounds for that, but that left the impression that Kamal was for bigger services than I was expecting.

# Enter Kamal v2 and [Kamal Proxy](https://github.com/basecamp/kamal-proxy)

Kamal v2 dropped Traefik for Kamal Proxy, which is an in-house made proxy that completely orchestrates the proxy between apps, even dealing with 0 downtime deployments, which is not a requirement for me on this website, but it's always nice to have. 

 Everything feels like a perfect fit; the user-facing complexity is minimal, and with two config files, I had my app up and running, with two commands: `kamal setup` and `kamal deploy`
 
 This website source code is available [here](https://github.com/rafamoreira/rafaelmc.net/) with all Kamal configurations and more. The current stack is much more simplified than my previous post too. It's just a very small Flask app, rendering HTML directly from Markdown, running on gunicorn, with a Caddy reverse proxy in front of it, serving the static files, which is overkill for this site, but why not. Caddy is simple enough, then finally Kamal proxy in front dealing with auto-renewing Let's Encrypt certificates. 
 
 Let's take a brief look at the Kamal config file:
```deploy.yml
# Name of your application. Used to uniquely configure containers.
service: rafaelmc

# Name of the container image.
image: rafamoreira/rafaelmc.net

# Deploy to these servers.
servers:
  web:
    - 49.12.202.223

# Enable SSL auto certification via Let's Encrypt (and allow for multiple apps on one server).
# Set ssl: false if using something like Cloudflare to terminate SSL (but keep host!).
proxy:
  ssl: true
  hosts:
    - www.rafaelmc.net
    - rafaelmc.net
  # kamal-proxy connects to your container over port 80, use `app_port` to specify a different port.
  app_port: 80

# Credentials for your image host.
registry:
  server: ghcr.io
  username: rafamoreira
  password:
    - KAMAL_REGISTRY_PASSWORD

# Configure builder setup.
builder:
  arch: amd64
```
That's it, I won't go over details as it's a very basic config, but realistic all you need for a simple setup is to change the ip, the image name, the hosts, and the registre user/pass, it can't get much simpler than that. The documentation on their website is very complete, so don't skimp on that.

I'm really hooked on Kamal. It's one of the most polished and streamlined experiences I've ever had with deployment tooling, like a 100x better version of old Capistrano (does Capistrano still exist?). 

I know very well that my use case is not very sophisticated, and probably Kubernetes does everything better than Kamal, but for my use case, the simplicity and polish are unbeatable. 

Kamal rekindled my interest in the 37signals sphere of influence. for ~12 years I was doing my main development in Ruby, using a lot of Rails, but when I got a new job at a Python shop, I basically abandoned all Ruby and went all in on Python. But Kamal, combined with the recent talks about nobuild from DHH, makes me want to give a shot to Rails 8, see if it still feels like home, or if it will be an awkward reencounter.
