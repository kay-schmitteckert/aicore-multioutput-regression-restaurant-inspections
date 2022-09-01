# Build and push Docker Images of the implementations for Training and Inference

AI Core will run the code for training (in *train.py*) and for serving (in *serve.py*)
each in a separate Docker container later on. Therefore, you first have to build the
Dockerfiles and push them to your Docker Hub repository.

To do that for the traininig part, change your working directory to *src/train/* in your
terminal. Notice there is a Dockerfile in this directory. Then run the
following command:

```bash
docker build -t <PATH-TO-DOCKERHUB-REPO>:<IMAGE-TAG> .
```

Here `<IMAGE-TAG>` is the tag you gave to your image as a name. Now push your Docker image
to the Docker Hub repository by running:

```bash
docker push docker.io/<PATH-TO-DOCKERHUB-REPO>:<IMAGE-TAG>
```

Follow the same steps for the serving part. Make sure to first change directory to
*src/serve/* and to use a tag for the serving Docker image that is different from the one
for training.

Once you pushed both Docker images, look at your repository in Docker Hub and double check that your images have been
pushed successfully.