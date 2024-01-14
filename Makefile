run: ## Build backup container
	docker build -t my-pyspark-app  .
	docker run --memory 12g -v ./output:/app/output my-pyspark-app