docker-compose up -d
sleep 30
until docker-compose exec app test -e ./result/doctors_list.csv 
do 
    sleep 10
    echo "File Not Ready : retrying in 10 s"
done
docker-compose cp app:./app/processed/ ./processed
echo "communications files retrieved"
docker-compose cp app:./app/result/ ./result
echo "query files retrieved"
docker-compose down 
docker volume rm $(docker volume ls -q)
docker rmi -f $(docker images -aq)
echo "space cleaned"