---
author: Rizky Maulana Nugraha
date: '2020-12-07'
description: I have demonstrate some amazing PyCharm capabilities for microservice
  based python debugging setup.
erpnext_id: /blog/docker/using-a-docker-compose-based-python-interpreter-in-pycharm
erpnext_modified: '2020-12-07'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Docker
thumbnail: https://maulana.id/images/uploads/screen-shot-2020-11-22-at-18.51.14.png
title: Using a Docker Compose-Based Python Interpreter in PyCharm
---

I was involved with different kinds of Django projects in the past. Back then the standard approach of attaching your debug interpreter was by creating a virtual environment in your python project. We debugged using PyCharm at that time. JetBrains generously gave us a free licence to use the whole suite of JetBrains tools as their way of supporting open source projects.

  


However, back then the notion of developing a Django project from inside a container was not so common. We already managed some of our projects as microservices described by one or more docker-compose files. To debug with this kind of setup, we used an SSH daemon inside our container. Then we setup PyCharm so that it treated the docker container as a **remote interpreter**. This worked for quite a long time (almost 5 years). Then finally JetBrains released support to allow interpreters inside a docker-compose configuration.

  


Things didn’t transition smoothly back then. The first issue that I remember is that the interpreter forgot all the environment variables declared in the docker-compose file. Since Django used environment variables to override its settings file, this setup was unusable. So we keep doing the old way, using a remote interpreter.

  


Recent PyCharm versions are making it more difficult to set up a remote interpreter. As of now, in version 2020.2, when we set up a remote interpreter, PyCharm implicitly defines a deployment configuration. This is not needed if you are using a container, because the files are already mounted there and you don’t need to copy them again using sftp, etc. However the new interface is quite confusing because you can’t disable the setting at first. You are only allowed to delete the deployment configuration after you’ve made the configuration (funny, eh?). I’ve also tried a different approach, such as creating the SSH configuration first, then set it as remote interpreter, but still it generates the deployment configuration.

  


So, fed up with this, I decided to try the docker-compose-based interpreter again. I noticed several improvements:

  1. You can now include multiple docker-compose recipes (useful for overriding local config on top of production config)
  2. You are allowed to include an environment file (they fixed the main deal breaker from the previous issue)
  3. You can map a local directory to a directory inside container (so that PyCharm knows it's the same thing)
  4. When you create a Run Configuration, the environment the interpreter uses is the one coming from docker-compose. So, you won’t need to redeclare your environment variables again. Hurray!



# Requirements

The article from here is going to be a sort of hands on lab/workshop. You can skim through, but it is best if you do it at your own pace.

  


We are going to assume this basic understanding of technical skills:

  1. Git and how to use it to clone a project from Github
  2. Docker, Docker-compose, and how to use their CLI
  3. Linux based environment, or MacOS, or WSL.
  4. Python and Django basic understanding
  5. Debugging methods/terminologies



  


In addition to that, since we are using PyCharm, you need PyCharm Pro Edition to use its debugging features.

  


# Usual setup without IDE

To demonstrate how PyCharm enhances our development workflow — and not ruining it or conflicting with the current workflow — I create a small sample repo here so you can see our basic [Django setup](<https://github.com/lucernae/django-ide-setup>). My explanations will refer to that repo. Clone the repo to start experimenting with it.

We are going to set up a small microservice-based django server. The repo contains two folders, `django_project` and `deployment`. The `deployment` folder contains an orchestration script to run the project. The `django_project` is where the actual Django app is located.

To run the project, we (by we, I mean my colleague and myself) usually go into the deployment folder and run `make` scripts to spin up the server. We don’t have those now since we want to be a bit more technical and dive in. We are going to run docker-compose directly.

  

    
    
    docker-compose up --build -d

  


This is just to warm up docker. We want to build our initial images and see them running. One good rule of thumb to help you later to set up a production build: Prepare one initial docker-compose that can be run immediately without having to do further customisation so that developers can easily check the code out.

  


If you open your browser and navigate to http://localhost/ . You will see the default welcome screen. It will only say `Welcome to localhost`.

Since using an IDE is a choice, I want to believe that running the project immediately should not depend heavily on the choice of IDE. The developer should be able to run this out of the box.

  


However, this is a minimal setup. When doing some custom development work, or deployment, you will have to change some deployment configuration. To illustrate this, I’ve prepared a simple template `.template.env` and `docker-compose.override.template.yml`.

But before we proceed, shut down the current stack first, since we are going to change the compose config.

  

    
    
    docker-compose down

Copy the file `.template.env` as just `.env`. This is a docker-compose environment config file. When interpolating variables in the docker-compose files, generally the precedence will be:

  


default value —> env file —> shell environment variables

  


This means if a variable is defined in the env file but not in the shell, then docker-compose will use whatever value defined in the env file. This is very flexible and supports declarative deployment. For example, in the previous docker-compose command, if you look at the basic recipe `docker-compose.yml`, you will see that we have defined environment variable inside django container to take a value from the shell with some default value:

  

    
    
    services:django:environment:DJANGO_SETTINGS_MODULE: mysite.settings
    
          DEBUG: ${DEBUG:-False}SITENAME: ${SITENAME:-localhost}

  


With this kind of variable passing, we can expect that the environment variables are accessible from within Django settings so we can make a fully config-based deployment.

  


Now look at the `.env` file you just copied.

  

    
    
    COMPOSE_PROJECT_NAME=mysiteCOMPOSE_FILE=docker-compose.ymlDEBUG=TrueSITENAME=myothersite.testDJANGO_HTTP_PORT=8080HTTP_PORT=80

  


We override some settings. Notably, the `DEBUG` variable to become `True` because we want to enable Django debug mode. You can experiment by changing other variables too. For the top two variables: `COMPOSE_PROJECT_NAME` and `COMPOSE_FILE` were docker-compose internal variables. Changing `COMPOSE_PROJECT_NAME` will change your docker-compose stack namespace (useful to quickly associate a stack with a project). Meanwhile, `COMPOSE_FILE` can control which docker-compose file are going to be included by `docker-compose` command.

  


We are going to create an extra compose file to override some deployment config. Change the value to `COMPOSE_FILE=docker-compose.yml:docker-compose.override.yml`. A useful note worth knowing, if you omit `COMPOSE_FILE` variable entirely (make it empty value), then `docker-compose` default behaviour is to look for `docker-compose.yml` and `docker-compose.override.yml` if it exists. By the way, the precedence matters. Rightmost file mentioned in the variable will override files on the left.

  


Now, create `docker-compose.override.yml` from the template `docker-compose.override.template.yml`.

  


You can see the content like this:

  

    
    
    version: '3'services:django:command: python manage.py runserver 0.0.0.0:8080volumes:- ../django_project:/home/web/django_project
    
      
    
    
      nginx:volumes:- ./sites-enabled:/etc/nginx/conf.d

  


Since we are going to be in ‘development mode’, we use django manage.py server. We also mount our local directory so the container will always have the latest changes in our files. We also mount nginx config in case we are dealing with production mode settings. You can even add more overrides like `environments` or `ports` depending on the need.

  


Now that we’re ready, spin up the stack (without rebuilding)

  

    
    
    docker-compose up -d

  


You can then check http://localhost:8080/ again. Now it says `Welcome to myothersite.test`, which is the value of `SITENAME` that we declared in the `.env` file. 

  


It will also spawn a Django debug server in port 8080 by default. We setup two server like this because Django debug server supports hot reload. So if you change code or templates, you may want to see the changes immediately. In that case, you can navigate to http://localhost:8080/ to see the changes.

This is as far as our native setup goes without IDE. Basically you do the development in the files in your host machine, but with the python and Django servers deployed using containers.

  


One other thing worth mentioning is how we run unittest. Since Django and Python are in a container, we run Django tests like this:

  

    
    
    docker-compose exec django python manage.py test

  


As you can see, the command becomes very long. That’s why we store `Makefiles` to provide shortcut commands in the deployment directory.

  


Before continuing the next section, don’t forget to shut down the stack

  

    
    
    docker-compose down

#   


# IDE Setup Using PyCharm

To see how much PyCharm improves our workflow, using the same repo, open the folder in PyCharm.

  


## Docker-compose setup

PyCharm bundles the docker-compose plugin integration by default. If for some reason you can’t use it, refer to [official doc](<https://www.jetbrains.com/help/pycharm/docker-compose.html>).

  


Open the `docker-compose.yml` file in the `deployment` directory. You will see that the lines are annotated by arrows like this:

![docker-compose.yml file](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-18.51.14.png)

  


You can click the arrow. Click the double arrow in the `services:` line. PyCharm will deploy that recipe for you. The service tab will appear to let you know that the compose file are deployed.

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-18.57.02.png)

  


As you can see, it also picks up the `COMPOSE_PROJECT_NAME` that you specify in the `.env` file. `mysite` is the name of the stack and you can drill down in it to see the services. This tab offer some controls too. You can redeploy, stop, or shut down the deployment with just a click. Right click the deployment name to see the context menu.

  


After some sightseeing you will notice that what you deploy (even though it picks up `.env` file) is only the recipe from `docker-compose.yml` file. It is evident if you see the service log of django, it shows uWSGI running and not Django debug server.

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-19.02.44.png)

  


So, edit the PyCharm configuration. You can do it from the deployment context menu then Edit Configuration, or deployment configuration bar on the top menu. Basically add the file `docker-compose.override.yml` in the Compose files field. So you will have something like this:

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-19.06.45.png)

  


Now you can spin up/down your deployment stack with just a button click from your Services tab. By clicking deploy, you can update your stack deployment and recreate a fresh service. It is now running using Django Debug Server.

  


It’s quite convenient now to edit your docker-compose file and apply the changes to the deployment.

  


In a typical development session, you mostly run the deployment once, do some coding, and then validate it and maybe do some debugging. So we are going to set up that workflow too.

## Python interpreter setup

We first setup the Python Interpreter.

  


Open PyCharm Project settings, then navigate to Project Interpreter. Click the gear icon and click Add. You will be given several options to select the source of your interpreter. Choose docker-compose. Fill in the settings, which consists of Configuration file(s) (Put `docker-compose.yml` and `docker-compose.override.yml` in that order), and the service (Pick `django`). 

  


It should look like in the image below. Click OK.

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-19.15.30.png)

  


It might take some time for PyCharm to build its custom images (with pycharm helpers inside the containers).

  


Next, you want to set project path mappings. The locations of code in your repo in your host computer are different from the locations **inside** the container. 

  


That’s why PyCharm needs to know the mappings. Specify the project path mappings. In our case we map `django_project` into `/home/web/django_project` inside the container. This is as reflected in the volume declarations of our `docker-compose.override.yml`. In your own project, you need to decide by yourself what are the paths that needed to be mapped out, because there can be more than one.

  


Screenshot below can be used as visual guide:

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-19.19.28.png)

  


Once you are done, click OK. Wait a bit for PyCharm to build the helper skeletons. Once it’s finish rebuilding, you can click **Python Console** tab to load the python console in PyCharm. 

  


This is the same Python interpreter that Django will use. You can also check that the variables from `.env` file carried over nicely as seen in the screenshots:

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-19.27.32.png)

  


Note that this is a Python interpreter, not Django shell. To use Django, you need to enable Django integration.

  


Open Project Settings again, type **Django** in the search bar**.** In the **Language and Frameworks** menu, select Django. Enable Django Support. Fill in all relevant information for your project. In our example, the Django project root is in `django_project` directory, and the settings module is in `mysite.settings`. 

  


See screenshot below for reference:

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-19.33.05.png)

  


After setting this up, whenever you navigate to the **Python Console** , you will get **Django Console** instead:

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-19.36.22.png)

  


It’s the same thing you get from running `docker-compose exec django python manage.py shell`. Isn’t that sweet? As you can see, the settings file and environment variables from `.env` are properly loaded and evaluated as Django settings.

## Django debug server setup

Now, let’s step up further and create a Django server run configuration.

  


Mark the `django_project` directory as a **Source Directory** by right clicking the directory and select **Mark Directory as** > **Sources Root** . If it’s not detected already, mark the `django_project/mysite/templates` directory as **Templates Folder**. You will now be able to activate code completions in that folder.

  


To create a new Run/Debug Config (for Django now), click the Configuration selector, or navigate from menu **Run** > **Edit Configuration**. As you can see, you already have docker-compose run configuration. We now want to add Django run config. Click the + button and choose **Django Server**. Most of our config resides in `.env` file. So we don’t actually need to modify anything else here besides the target server address to match the port that we expose in the container (currently 8080). See the screenshot for reference:

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-19.48.18.png)

  


Click OK. Then you can click the Run Button with **Django** config selected (or whatever the name you gave for the config in previous step). Run button will run the Django Debug Server as usual, meanwhile Debug button will attach the PyCharm debugger to Django. Let’s check what the Debug button does.

  


The Debug mode panel will show up after you click the Debug button. It basically recreates a service to attach the debugger. You can also see the log in that panel, which is nice because you don’t need to go inside the container to see that now.

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-19.51.18.png)

  


As with any debugging session, you can attach breakpoints to any of your python code in the sources folder. With PyCharm you can even attach breakpoints in the template! You can debug in realtime when the template is currently rendered. This is such an awesome feature. Here’s what it looks like when you are currently debugging Django Template:

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-20.05.03.png)

  


You can do many things in this mode, such as inspecting variables and so on. If for some reason this template debugger doesn’t work for you, check out the [documentation](<https://www.jetbrains.com/help/pycharm/templates.html>) and make sure that you set the current template language to be Django instead of Jinja.

  


## Test runner setup

Then, the next tips that I would like to add is about running Django test.

  


One of the ways is to click your test file or test folders, or even the whole Django app module, then right click, then click Run test from the context menu. It will create a Run test configuration and run it. Since all of our configs are declarative in the `.env` file, we don’t need to edit the config, unless you need to modify specific settings. Here’s what it looks like when we do that.

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-20.17.56.png)

  


As another way of running the test, if you need just to run a single specific test, you can click the arrow button (also can be seen in the screenshot) in the line where the specific test method is declared in the test file. Then PyCharm will run only that.

  


## Some (optional) beta setups

Finally, my last tips here are some things that I am really waiting for in PyCharm. 

  


From my conversation with @gamesbrainiac in twitter: <https://twitter.com/gamesbrainiac/status/1320793098658762753>, it seems you can store a Run configuration as a file now. So, if your project is complex and you have crafted a specific run configuration, you can share it to the other devs in your team as well. Especially if the deployment is exactly the same (because we are using a declarative docker-based deployment). You can use it to allow developers to deploy the latest changes to the staging server with just a click. However this is more of a devops-related topic. So, in general you can share a run config to allow your colleague to run unittest or local deployment the exact same way. Just make sure that you don’t store sensitive data in it.

  


To demonstrate how feasible is this, first let us imagine that we haven’t made any run configuration. We want to use what’s already been given in the repository. Open the repo inside PyCharm. The Run Configuration list will be empty. However, if there are run configurations in the repo, they can be detected. First open the Edit Configuration menu. As you can see there are three broken Configurations:

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-20.41.53.png)

  


For the docker-compose configuration there is no other editing needed so you can just click OK and run the config.

  


For Django-based config, you need to enable Django support in the project settings first. The dialog conveniently gives you a **Fix** button so you can click on it.

![](https://maulana.id/images/uploads/screen-shot-2020-11-22-at-20.46.12.png)

  


Proceed to fix the problem by following the wizard. Typically what you need to do is define the interpreter again and enable Django support. After that you can run the config again.

  


I have somewhat conflicting opinions on this share run configuration thing. This kind of workflow seems pretty promising, but at the moment it feels like a beta feature and not solid enough. What it lacks at the moment is to store the interpreter information in a modular way, so it can be imported easily. This feature is also not easily discoverable. If you store your run config as a file and persist it in a git repo, then your colleague can only discover it by opening the file and noticing that PyCharm gives a warning that it is a run configuration file, from which you can proceed by clicking the warning and making it available in your local PyCharm installations. So take this last tip as optional beta.

  


When this feature is solid enough, I think it is going to make PyCharm the ideal Python IDE to collaborate. Imagine we just put the config inside the repo and then your colleague can just do first setup with relative ease to run the project. Totally incredible.

  


# Conclusions

I have demonstrated some amazing PyCharm capabilities for microservice based python debugging setup. It also has a potential to be a one stop shop for creating a unified IDE setup for a team of developers, which can be productive for projects where the developers come and go. This will enable new developers to get in the workflow much easily, as everything has already been prepared from the start.

  


It’s also important to notice that this seamless integration is only possible if your project setup is declarative from the start. It’s also ok for developers who are not using PyCharm to start the project, but the developer who uses PyCharm gets to use the same exact configuration. So that means, even though they have different methods when they do their own development, they share the same, repeatable project config. It will allow them to use the same config and tailor it for their own specific IDE.

# Note

This article was originally generated using GatsbyJS in my own personal blog here: <https://maulana.id/2020--11--20--10--using-docker-compose-based-python-interpreter-in-pycharm/>
