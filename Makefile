start: build run

build:
	docker build -t your_project_name:latest .

run:
	docker run -p 5000:5000 your_project_name:latest
