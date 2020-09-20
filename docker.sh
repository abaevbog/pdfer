docker run -d \
  -it \
  --mount type=bind,source=/Users/bogdanabaev/RandomProgramming/BasementRemodeling/PDFER,target=/home \
  -p 80:80 \
  pdfer:latest