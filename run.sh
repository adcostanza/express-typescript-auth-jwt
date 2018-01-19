tsc
docker-compose up -d db
host=localhost \
secret='630ba2d52134be796df40b065fc0' \
user='adam' \
pw='tacos' \
node dist/main.js
