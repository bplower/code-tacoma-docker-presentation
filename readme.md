
# Introduction to Docker

This repository demonstrates some of the basics of docker and docker-compose through the use of a simple flask API backed with a database.

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
Traceback (most recent call last):
  File "/usr/local/bin/buildings-api", line 11, in <module>
    sys.exit(main())
  File "/usr/local/lib/python3.7/site-packages/buildings_api.py", line 87, in main
    app = BuildingsApi(config_path)
  File "/usr/local/lib/python3.7/site-packages/buildings_api.py", line 22, in __init__
    self.app_config = load_config(config_path)
  File "/usr/local/lib/python3.7/site-packages/buildings_api.py", line 65, in load_config
    with open(cfg_path, 'r') as stream:
FileNotFoundError: [Errno 2] No such file or directory: 'settings.py'
```

Boooooo! This isn't what we want! Our application is expecting a configuration file at the path "/app/settings.yml" within the container, but that file wasn't included when the image was built. This was intentional because including such a file would be roughly equivalent to hardcoding settings in code itself. Now we need to run our docker container and give it access to a local configuration file to use:

```
brahm@localhost ~/buildings-api $ docker run -v $(pwd)/settings.example.yml:/app/settings.yml:ro buildings-api
Traceback (most recent call last):
  File "/usr/local/bin/buildings-api", line 11, in <module>
    sys.exit(main())
  File "/usr/local/lib/python3.7/site-packages/buildings_api.py", line 87, in main
    app = BuildingsApi(config_path)
  File "/usr/local/lib/python3.7/site-packages/buildings_api.py", line 24, in __init__
    self.db_pool = ThreadedConnectionPool(1, 20, **self.app_config['db'])
  File "/usr/local/lib/python3.7/site-packages/psycopg2/pool.py", line 161, in __init__
    self, minconn, maxconn, *args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/psycopg2/pool.py", line 58, in __init__
    self._connect()
  File "/usr/local/lib/python3.7/site-packages/psycopg2/pool.py", line 62, in _connect
    conn = psycopg2.connect(*self._args, **self._kwargs)
  File "/usr/local/lib/python3.7/site-packages/psycopg2/__init__.py", line 130, in connect
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
psycopg2.OperationalError: could not connect to server: Connection refused
	Is the server running on host "localhost" (127.0.0.1) and accepting
	TCP/IP connections on port 5432?
could not connect to server: Cannot assign requested address
	Is the server running on host "localhost" (::1) and accepting
	TCP/IP connections on port 5432?
```

The server failed to start completely, but not because of configuration file problems- we simply can't connect to the database to initialize our connection pool. Lets talk about what we just did for a moment before moving forward. We've included a simple form of the volume (`-v`) option while calling docker run. Here we've taken the path of the `settings.example.yml` file and mounted it to the `/app/settings.yml` path inside the container- exactly where our server expects it to be. Lastly, we included the `:ro` label, which indicates that the volume should be mounted within the container as read-only. This is a good security practice since you don't want anything (or anyone) in the container to be able to change this file. I would recommend reading the [official documentation](https://docs.docker.com/storage/volumes/) on the volume option since it provides much more functionality than is used here.

## Building via Docker Compose

Docker compose can make the process of building an image easier. If you look at the `docker-compose.yml` file, you'll see that we've defined a service called "buildings-api". That service has information about where the dockerfile is located, what volumes to mount, and what ports to forward. All of this information would have otherwise been provided on the commandline, but instead we can simply build our image by running:

```
docker-compose build api
```

## Running via Docker Compose

Running our image via docker-compose is just as simple as building it via docker compose. If we want to run our image by itself, we can say:

```
brahm@localhost ~/buildings-api $ docker-compose up api
docker-presentation_db_1 is up-to-date
Creating docker-presentation_api_1 ... done
Attaching to docker-presentation_api_1
api_1  | Traceback (most recent call last):
api_1  |   File "/usr/local/bin/buildings-api", line 11, in <module>
api_1  |     sys.exit(main())
api_1  |   File "/usr/local/lib/python3.7/site-packages/buildings_api.py", line 87, in main
api_1  |     app = BuildingsApi(config_path)
api_1  |   File "/usr/local/lib/python3.7/site-packages/buildings_api.py", line 24, in __init__
api_1  |     self.db_pool = ThreadedConnectionPool(1, 20, **self.app_config['db'])
api_1  |   File "/usr/local/lib/python3.7/site-packages/psycopg2/pool.py", line 161, in __init__
api_1  |     self, minconn, maxconn, *args, **kwargs)
api_1  |   File "/usr/local/lib/python3.7/site-packages/psycopg2/pool.py", line 58, in __init__
api_1  |     self._connect()
api_1  |   File "/usr/local/lib/python3.7/site-packages/psycopg2/pool.py", line 62, in _connect
api_1  |     conn = psycopg2.connect(*self._args, **self._kwargs)
api_1  |   File "/usr/local/lib/python3.7/site-packages/psycopg2/__init__.py", line 130, in connect
api_1  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
api_1  | psycopg2.OperationalError: could not connect to server: Connection refused
api_1  | 	Is the server running on host "db" (127.0.0.1) and accepting
api_1  | 	TCP/IP connections on port 5432?
api_1  | could not connect to server: Cannot assign requested address
api_1  | 	Is the server running on host "db" (::1) and accepting
api_1  | 	TCP/IP connections on port 5432?
api_1  |
docker-presentation_api_1 exited with code 1
```

Like before, we get the error message saying we aren't able to connect to the database. This was to be expected. Docker compose make running multiple services together very easy though. Lets instead simply run `docker-compose up`, which will start the database along with the api. It's worth noting here that docker-compose is mounting the settings file here in the root directory of the project rather than the example settings file. There's a small difference between the two: the database hostname is set to "db" here. When docker-compose runs the two containers together, it ensures they can communicate with each other based on their service names. Since the database service name is "db", it can be resolved on the network as "db".

Now that the service is running, lets verify we can actually communicate with it. In another terminal we should see the following:

```
brahm@localhost ~/ $ curl http://localhost:9090/
{'message':'Hello world!'}%
```

This is also a good example of how ports can be forwarded through to containers. In the settings.yml file, you'll see that we've told the service to listen on port 8080, but when we try to talk to it, we end up talking to it on port 9090. That's because docker is forwarding port 9090 on your host to port 8080 on the container.

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

## Tooling glossery

- Docker
- [Docker volumes](https://docs.docker.com/storage/volumes/)
- Docker compose
- Python's virtualenv
