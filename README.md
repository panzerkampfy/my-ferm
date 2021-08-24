# my-ferm

docker-compose -f local.yml up -d

docker-compose -f test.yml up --build --force-recreate --remove-orphans --abort-on-container-exit


docker-compose -f local.yml logs
