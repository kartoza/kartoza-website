---
author: Boney Bun
date: '2018-06-21'
description: Introduction Another doc about SSL? Maybe... We are writing this to explain
  our trial and error on setup SSL on the servers. You might have
erpnext_id: /blog/uncategorised/how-to-setup-ssl-on-nginx-using-letsencrypt
erpnext_modified: '2018-06-21'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Uncategorised
thumbnail: /img/blog/placeholder.png
title: How to Setup SSL on Nginx Using LetsEncrypt
---

### Introduction

Another doc about SSL? Maybe... We are writing this to explain our trial and error on setup SSL on the servers. You might have read somewhere about setting up SSL (so have we, and it's painful).  
Our blog is based on hands-on experience and hopefully you can learn something from it.

We assume that you already have your web server up and running. Suppose that your domain name is: example.com. You are thinking that it's time for you to enhance the web server's security by adding the SSL protocol.

There are various options for how to configure your web server. We assume you have [NGINX](<https://www.nginx.com/>) as your reverse proxy and that your apps are behind the proxy. We also use Let's Encrypt (LE) as the Certificate Authority (CA) provider. Hence, certbot is chosen as the software to bridge between our server and LE's server.

We start with a short version following by a long one.

### Setting up SSL - short version

In short, you will need to obtain the certificate and configure NGINX.

**Install certbot on your server (also known as letsencrypt or letsencrypt-auto on older version) to obtain the certificate:**  
\- Go to **<https://certbot.eff.org>**  
\- On the site, select Nginx in **Software section** and your OS in the **System section** (in our case: Ubuntu 16.04).
\- There will be an explanation on how to install certbot. Follow the steps and certbot will be on your system.

Alternatively, you may find certbot in Docker is more convenient. Download and dockerise certbot by typing this command:
`docker run -it --rm --name certbot -v "/etc/letsencrypt:/etc/letsencrypt" -v "/var/lib/letsencrypt:/var/lib/letsencrypt" certbot/certbot certonly`

The command above will download certbot and run the software to obtain the certificate from LE.

**Running certbot**  
`sudo certbot --nginx`

The command above will verify that you have sufficient permission on the domain you claimed, then it will obtain the certificate for your domain. Finally, certbot will automatically update your nginx's configuration. No hassle...  
****

**Restart NGINX**

Restart your NGINX so the new config file can be reloaded: `sudo service nginx restart`

Voila! Your system has been upgraded to using https protocol.

### Setting up SSL - long version

The certbot installation should be pretty straightforward and simple. We are sorry if you reach this section as you might find something went wrong on the server.  
Never mind... we also had the same problem. That's the main reason we wrote this article.

Let us step back and do the process manually. We will need to configure the nginx first. Then, obtain the certicate from LE. Finally, we have to make some adjustments to the nginx configuration file.

#### Install On Your Machine

##### Configure NGINX

You may have a hard time giving LE access to your server during the verification process. This is where you really need to understand your server as one may differ from another.

The main task is to make sure that LE can access the following url: **<http://example.com/.well-known/acme-challenge>.**LE will try to add new file in the folder during the verification process.  
If it succeeds, the certificate can be issued. Otherwise, certbot will stop.

To give LE access to your server, make sure you have these lines on your nginx' config file:

    ...  
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
    ...

You can test your new config by typing the following command: `nginx -t`  
Make sure nginx is not complaining before proceed to the next step.  
Next, you need to restart nginx: `sudo service nginx restart`

##### Obtain the certificate

We suggest that you use `--test-cert` when trying to obtain the certificate.

`--test-cert` basically tells LE to use its staging server, instead of its production server.

The production server limits a certificate request of 20 request per week (<https://letsencrypt.org/docs/rate-limits/>). If you manage to obtain a certificate in a single shot, congratulations!

But, if you still doubt that you will obtain the certificate, `--test-cert` will save your day.

There is no limit for requesting a certificate from staging server.

Now, as you know the restriction, you can type:  
_****_`certbot certonly --test-cert --webroot -w /home/web/example.com/deployment/webroot-path -d example.com`

Once LE is happy and gives you a certificate, you can try the same command without `--test-cert`.

##### Modify the NGINX config file

Congratulations! You have the certificate for your domain now.

By default, the certificate can be found on: _**/etc/letsencrypts/live/ <your_domain_name>. **_

Thus, your nginx needs to be aware of the certificate and listen on port 443.

Also, it's time to redirect a request from port 80 to port 443.

Add the following lines to your nginx config file:

    server {  
     ...  
     # the port your site will be served on  
     listen 443 ssl;  
     # the domain name it will serve for  
     server_name example.com;  
      
     ssl on;  
     ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;  
     ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;  
     ssl_protocols TLSv1 TLSv1.1 TLSv1.2;  
     ssl_prefer_server_ciphers on;  
     ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';  
      
     location /.well-known/acme-challenge {  
     default_type "text/plain";  
     # set to webroot path  
     root /var/www/webroot;  
     }  
     ...  
    }  
    server {  
     # tells nginx to redirected http request to https  
     listen 80;  
     server_name example.com;  
     return 301 https://$host$request_uri;}  
    ...

Restart your nginx for the new change to take effect.

All is good now :)
