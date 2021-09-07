pipeline{
	agent any
	stages{
		stage("Build") {
			steps{
				echo "building the container now..."
				sh "docker build --tag my-app:v1.0 ."
				sh "docker run -d -p 7000:5000 --env-file /home/smadabat/Documents/test/.env my-app:v1.0"
				echo "successfully built the container and is running in 7000 port"
			}
		}
		stage("Test") {
			steps{
				sh "curl -G http://localhost:7000/get"
			}
		}
	}
}
