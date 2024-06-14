## OpenFGA Example
Example code to run OpenFGA. After install RestClient Extention, you can open file restapi.http and click api name to run command.

initial steps

- from restapi.http run command create store

## Prerequisite

install vitual studio code \
https://code.visualstudio.com/

install REST Client on visualstudio \
https://marketplace.visualstudio.com/items?itemName=humao.rest-client


## Run project

```bash
# start project
docker compose up --build
```

## Domain list

Playgroud: \
http://localhost:3000/playground

Rest API: \
http://localhost:8080

## Get json file from DSL 
open folder transformer check file source/model/autherization_model.dsl
```bash
# run this command to tranform file from autherization_model.dsl to autherization_model.json
docker exec -it transformer npx @openfga/syntax-transformer transform --from=dsl --inputFile=autherization_model.openfga
```