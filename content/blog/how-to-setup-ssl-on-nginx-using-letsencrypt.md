---
title: "How to Setup SSL on Nginx Using LetsEncrypt"
description: "Another doc about SSL? Maybe... We are writing this to explain our trial and error on setup SSL on the servers."
tags:
  - Hosting
  - SSL
  - Nginx
date: 2018-06-21
author: "Boney Bun"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="How to Setup SSL on Nginx Using LetsEncrypt"
    subtitle="Hosting"
    class="is-primary"
    sub-block-side="bottom"
>}}
Another doc about SSL? Maybe... We are writing this to explain our trial and error on setup SSL on the servers.
{{< /block >}}

## Introduction

Another documentation about SSL certificates? Perhaps. This article documents the practical experience gained while configuring SSL on servers. While SSL setup information exists elsewhere, this guide shares real-world troubleshooting insights.

The guide assumes you already have an operational web server with a domain name (e.g., example.com) and want to enhance security by implementing the SSL protocol.

The setup uses Nginx as a reverse proxy with applications behind it, and Let's Encrypt as the Certificate Authority, with certbot bridging the connection.

## Setting up SSL - Short Version

Two main steps are required: obtaining the certificate and configuring Nginx.

**Install Certbot:**
- Visit https://certbot.eff.org
- Select Nginx under Software and your OS under System (e.g., Ubuntu 16.04)
- Follow installation instructions

Alternative Docker approach:
```bash
docker run -it --rm --name certbot -v "/etc/letsencrypt:/etc/letsencrypt" -v "/var/lib/letsencrypt:/var/lib/letsencrypt" certbot/certbot certonly
```

**Running Certbot:**
```bash
sudo certbot --nginx
```

This command verifies domain ownership, obtains the certificate, and automatically updates Nginx configuration.

**Restart Nginx:**
```bash
sudo service nginx restart
```

Your system now uses HTTPS protocol.

## Setting up SSL - Long Version

Certbot installation is typically straightforward, but issues may arise on some servers. This section addresses manual configuration.

### Configure Nginx

The key challenge involves granting Let's Encrypt access to verify domain ownership. Let's Encrypt must access: **http://example.com/.well-known/acme-challenge** and create verification files there.

Add this to your Nginx config:

```nginx
server {
 ...
 server_name example.com;
 listen 80;
 ...
 location /.well-known/acme-challenge {
     default_type "text/plain";
     root /var/www/webroot;
 }
 ...
}
```

Test configuration:
```bash
nginx -t
```

Restart Nginx:
```bash
sudo service nginx restart
```

### Obtain the Certificate

Use the `--test-cert` flag initially to utilize Let's Encrypt's staging server (unlimited requests). Production servers enforce a 20-request-per-week limit.

```bash
certbot certonly --test-cert --webroot -w /home/web/example.com/deployment/webroot-path -d example.com
```

Once successful, run the same command without `--test-cert`.

### Modify the Nginx Config File

Certificates are located at: **/etc/letsencrypt/live/<domain_name>**

Add these lines to enable HTTPS and redirect HTTP traffic:

```nginx
server {
 ...
 listen 443 ssl;
 server_name example.com;

 ssl on;
 ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
 ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
 ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
 ssl_prefer_server_ciphers on;
 ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';

 location /.well-known/acme-challenge {
 default_type "text/plain";
 root /var/www/webroot;
 }
 ...
}

server {
 listen 80;
 server_name example.com;
 return 301 https://$host$request_uri;
}
```

Restart Nginx to apply changes. Configuration complete.
