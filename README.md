# k8s-apps

## Usage

```sh
docker build -t <docker-username>k8s-app-$(date +%s) -f Dockerfile .
docker login
docker push
```

After push to docker hub, application will be deploy to k8s
