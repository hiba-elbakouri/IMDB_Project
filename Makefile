run: ## Build backup container
	docker build -t my-pyspark-app  .
	docker run --memory 12g -v ./output:/app/output -p 8076:5000 my-pyspark-app
