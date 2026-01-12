

# MDB Platform

Distributed application of mdb running across multiple Docker containers.

## Getting started

Download [Docker Desktop](https://www.docker.com/products/docker-desktop) for Mac or Windows. [Docker Compose](https://docs.docker.com/compose) will be automatically installed. On Linux, make sure you have the latest version of [Compose](https://docs.docker.com/compose/install/).

This solution uses Java Spring, Angular, ReactJS, Python, Node.js, with Redis for messaging and Postgres for storage.

Run in this directory to build and run the app:

```shell
docker compose up
```

The `mdb-web-app` app will be running at [http://localhost:4200](http://localhost:4200), and the `admin-web-app` will be at [http://localhost:3200](http://localhost:3200).


