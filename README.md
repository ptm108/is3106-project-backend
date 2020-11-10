# S A S H I M I

Sashimi is developed under NUS's School of Computing IS3106 Module. Sashimi is a collective group-buy platform for groceries to be delivered to your doorstop. The tech stack powering Sashimi's backend comprises of Django, Django Rest Framework, PostgreSQL as our RDB.

<img src="https://www.djangoproject.com/m/img/logos/django-logo-positive.png" width="100"> <img src="https://zdnet2.cbsistatic.com/hub/i/r/2018/04/19/092cbf81-acac-4f3a-91a1-5a26abc1721f/thumbnail/770x578/5d78c50199e6a9242367b37892be8057/postgresql-logo.png" width="100"> <img src="https://www.django-rest-framework.org/img/logo.png" width="100">

## Local setup

We are using docker containers for fast local deployment with minimal installations.

| Prerequisites  | Version | Links |
| -------------- | ------- | ----- |
| Docker Desktop | 19.03.13 | [Link](https://www.docker.com/products/docker-desktop) |

### To deploy locally

Clone this repository

``` bash
git clone git@github.com:ptm108/is3106-project-backend.git
```

*Before you start, get the `.env.dev` file from TM or Eliz and place it in the `root folder`*

Ensure that Docker Desktop is up and running.
<br/><br/>

### When setting up for the first time:

We will need to build the docker image and deploy it.

Build the docker image:

``` bash
docker-compose build
```

Run the docker container:

``` bash
docker-compose up -d
```

The backend is accessible at `localhost:8000`

---

To access admin panel on Django, you need to create a superuser:

``` bash
docker-compose exec web python manage.py createsuperuser
```

Follow the instructions to set up authentication details for the admin panel.

The admin panel is accessible at `localhost:8000/admin`

---

To undeploy docker container: (*Add -v flag to spin down postgres volume. Warning: database will be wiped*)

``` bash
docker-compose down
```
