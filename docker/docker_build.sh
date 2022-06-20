aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 612185335394.dkr.ecr.us-east-1.amazonaws.com
docker build -t 612185335394.dkr.ecr.us-east-1.amazonaws.com/pdfer .
docker push 612185335394.dkr.ecr.us-east-1.amazonaws.com/pdfer

   