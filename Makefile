IMAGE_NAME := awscli-slack
EXPOSEPORT := 5002
TAG := local

help:	## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build:			## Build awscli-slack app and cron service.
	docker build -t $(IMAGE_NAME):$(TAG) -f docker/Dockerfile-app .

run-app:		## Run awscli-slack app Service.
	docker run -it --rm -p 5002:$(EXPOSEPORT) $(IMAGE_NAME):$(TAG)
