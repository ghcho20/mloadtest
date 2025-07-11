# 환경 설정

## Prerequisites

- docker
- docker compose
- git

## 기본 테스트

- clone this repo to a local host(load tester)
- `cd mloadtest`
- create a `.env` file
- add `CLUSTER_URL=<MongoDB connection URI>` to _.env_ file
  > eg. `CLUSTER_URL=mongodb+srv://<db_username>:<db_password>@up.icpitla.mongodb.net/?retryWrites=true&w=majority&minPoolSize=100` for Atlas
- `docker compose up -d`
- open `http://<locust host>:8089` in a browser

<img src="./start.jpg" width="640">

- configure
  > - `Number of users`
  > - `Ramp up` (how long it will take to load total users in seconds)
  > - `Host`: **무시**
  > - Advanced options
  >   - `run time`
  >   - `Profile`: short description for this run
- click on `START`
