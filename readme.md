
# Introduction to Docker

This repository demonstrates some of the basics of docker and docker-compose through the use of a simple flask API backed with a database.

- [Building via Docker](https://github.com/bplower/code-tacoma-docker-presentation#building-via-docker)
- [Running via Docker](https://github.com/bplower/code-tacoma-docker-presentation#running-via-docker)
- [Building via Docker Compose](https://github.com/bplower/code-tacoma-docker-presentation#building-via-docker-compose)
- [Running via Docker Compose](https://github.com/bplower/code-tacoma-docker-presentation#running-via-docker-compose)
- [Databae initialization](https://github.com/bplower/code-tacoma-docker-presentation#database-initialization)
- [Local development](https://github.com/bplower/code-tacoma-docker-presentation#local-development)
- [Tooling glossary](https://github.com/bplower/code-tacoma-docker-presentation#tooling-glossary)

## Building via Docker

From the `buildings-api` directory, you can build the image by running:

```
docker build .
```

You can verify the image has been built by listing the images:

```
brahm@localhost ~/buildings-api $ docker image ls
REPOSITORY                                                      TAG                 IMAGE ID            CREATED             SIZE
<none>                                                          <none>              f0e9c51a0387        41 seconds ago      164MB
```

Our image has been built, but it doesn't have a name, so we can only reference it via the image hash. Referencing "f0e9c51a0387" isn't very clear, so we're going to rebuild the image with a proper name:

```
docker build . -t buildings-api
```

The end of the output will look something like the following:

```
 ---> Using cache
 ---> f0e9c51a0387
Successfully built f0e9c51a0387
Successfully tagged buildings-api:latest
```

The name of the image just a fancy tag. The tag "latest" was applied since we didn't specify any sort of version. We can specify a proper version number like so:

```
docker build . -t buildings-api:0.1.0
```

If we list our images, we'll see that the hash referenced by `buildings-api:latest` and `buildings-api:0.1.0` is the same, indicating that they are the exact same image, just with different tags.

```
brahm@localhost ~/buildings-api $ docker image ls
REPOSITORY                                                      TAG                 IMAGE ID            CREATED             SIZE
buildings-api                                                   0.1.0               f0e9c51a0387        9 minutes ago       164MB
buildings-api                                                   latest              f0e9c51a0387        9 minutes ago       164MB
```

## Running via Docker

Now that we have our docker image, let run it! The process of running the image effectively creates an instance of the image, which is called a container.

```
brahm@localhost ~/buildings-api $ docker run buildings-api
No such file or directory: 'settings.yml'
```

Boooooo! This isn't what we want! Our application is expecting a configuration file at the path "/app/settings.yml" within the container, but that file wasn't included when the image was built. This was intentional because including such a file would be roughly equivalent to hardcoding settings in code itself. Now we need to run our docker container and give it access to a local configuration file to use:

```
brahm@localhost ~/buildings-api $ docker run -v $(pwd)/settings.example.yml:/app/settings.yml:ro buildings-api
Failed to connect to database.
```

The server failed to start completely, but not because of configuration file problems- we simply can't connect to the database to initialize our connection pool. Lets talk about what we just did for a moment before moving forward. We've included a simple form of the volume (`-v`) option while calling docker run. Here we've taken the path of the `settings.example.yml` file and mounted it to the `/app/settings.yml` path inside the container- exactly where our server expects it to be. Lastly, we included the `:ro` label, which indicates that the volume should be mounted within the container as read-only. This is a good security practice since you don't want anything (or anyone) in the container to be able to change this file. I would recommend reading the [official documentation](https://docs.docker.com/storage/volumes/) on the volume option since it provides much more functionality than is used here.

## Building via Docker Compose

Docker compose can make the process of building an image easier. If you look at the `docker-compose.yml` file, you'll see that we've defined a service called "buildings-api". That service has information about where the dockerfile is located, what volumes to mount, and what ports to forward. All of this information would have otherwise been provided on the commandline, but instead we can simply build our image by running:

```
docker-compose build api
```

## Running via Docker Compose

Run the service and its dependent services via the "up" command:

```
docker-compose up
```

It's worth noting here that docker-compose is mounting the settings file here in the root directory of the project rather than the example settings file. There's a small difference between the two: the database hostname is set to "db" here. When docker-compose runs the two containers together, it ensures they can communicate with each other based on their service names. Since the database service name is "db", it can be resolved on the network as "db".

<aside class="notice">
The api container may fail here the first time you run this. The database takes a moment to initialize for the first time, and the api service will likely attempt to connect before the database is actually listening for connections. There are ways around this, but that's outside the scope of this tutorial. In our case, cancel the process (ctrl+c) and run it again and the database should start up in time.
</aside>

Now that the service is running, lets verify we can actually communicate with it. In another terminal we should see the following:

```
brahm@localhost ~/ $ curl http://localhost:9090/
{'message':'Hello world!'}%
```

This is also a good example of how ports can be forwarded through to containers. In the settings.yml file, you'll see that we've told the service to listen on port 8080, but when we try to talk to it, we end up talking to it on port 9090. That's because docker is forwarding port 9090 on your host to port 8080 on the container.

## Database initialization

At this point if we try to query the list of buildings, we'll recieve a 500 error since we haven't initialized our database yet. While you have `docker-compose up` running, in another terminal, run the following make targets:

```
make db-init
make db-load
```

This will create the "buildings" table in the database and add some very basic data to it.

Now we'll recieve some proper data when we query the api:

```
brahm@localhost ~/ $ curl http://localhost:9090/buildings/6
{'id': 6, 'name': 'One World Trade Center', 'height': 541, 'city': 'New York City', 'country': 'United States'}%
```

## Local development

Whenever testing `buildings-api` locally, install it within a python virtual environment to avoid polluting your local system.

```
virtualenv -p python3 venv
source venv/bin/activate
```

Now you can install the server within your virtual environment, and verify it runs as expected. Installing the package make the `buildings-api` executable available in your path.

```
pip install buildings-api/
buildings-api buildings-api/settings.example.yml
```

The application expects the path to a settings file as its first argument. An example settings file is provided in the buildings-api directory. For additional information about the buildings-api application and its settings, see the readme in the buildings-api directory.

## Tooling glossary

This is just a list of links to additional information about tools or features used in this project. This list may be incomplete and will expand as I have more time.

- Docker
- [Docker volumes](https://docs.docker.com/storage/volumes/)
- Docker compose
- Python's virtualenv
