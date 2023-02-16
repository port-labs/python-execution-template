## Table of Contents
1. [Local Setup](#Localhost)
2. [Webhook Setup](#Webhook)
3. [Port Setup](#Port)

### Localhost

1. Make sure that the Docker daemon is available and running
```
$ docker info
```

2. Create `.env` file with the required environment variables
```
$ cat .env

PORT_CLIENT_ID=<PORT_CLIENT_ID>
PORT_CLIENT_SECRET=<PORT_CLIENT_SECRET>
```

3. Build example's Docker image
```
$ docker build -t getport.io/port-execution-template .
```
:::note
add --platform linux/amd64 for M1 
:::

4. Run example's Docker image with `.env`

```
$ docker run -d --name execution_runner -p 80:80 --env-file .env getport.io/port-execution-template
```

5. Verify that the Docker container is up and running, and ready to listen for new webhooks:
```
$ docker logs -f execution_runner

...
[2022-09-18 12:17:17 +0000] [1] [INFO] Starting gunicorn 20.1.0
[2022-09-18 12:17:17 +0000] [1] [INFO] Listening at: http://0.0.0.0:80 (1)
[2022-09-18 12:17:17 +0000] [1] [INFO] Using worker: uvicorn.workers.UvicornWorker
[2022-09-18 12:17:17 +0000] [10] [INFO] Booting worker with pid: 10
...
[2022-09-18 12:17:19 +0000] [18] [INFO] Application startup complete.
```

`docker logs -f` command follows log output, and helps you also to troubleshoot future action runs.

### Webhook

1. Create public URL for your local application. 

In this tutorial, we create a new channel in [smee.io](https://smee.io/), and use provided `Webhook Proxy URL`. 

2. Install the Smee client:
```
$ pip install pysmee
```

3. Use installed `pysmee` client to forward the events to your localhost API URL (replace `<SMEE_WEBHOOK_PROXY_URL>`):
```
pysmee forward <SMEE_WEBHOOK_PROXY_URL> http://localhost:80/api/permission
```
