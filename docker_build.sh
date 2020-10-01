$(aws ecr get-login --no-include-email)
docker build -t 612185335394.dkr.ecr.us-east-1.amazonaws.com/pdfer .
docker push 612185335394.dkr.ecr.us-east-1.amazonaws.com/pdfer

   