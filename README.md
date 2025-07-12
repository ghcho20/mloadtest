### Contents

**&rarr; [환경 설정](#환경-설정)** <br>
**&rarr; [Preloading collection](#preloading-data)**

---

### 환경 설정

#### Prerequisites

- docker
- docker compose
- git

#### 기본 테스트

- clone this repo to a local host(load tester)
- `cd mloadtest`
- create a `.env` file
- add `CLUSTER_URL=<MongoDB connection URI>` to _.env_ file
  > eg. `CLUSTER_URL=mongodb+srv://<db_username>:<db_password>@up.icpitla.mongodb.net/?retryWrites=true&w=majority&minPoolSize=100` for Atlas
- `docker-compose -f docker-compose.envcheck.yml up -d`
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

#### Logging

To redirect container logging to both `stdout` & a file

> `docker logs -f <container name> 2>&1 | tee <log file name>`

#### Terminate

`docker-compose -f docker-compose.envcheck.yml down`

---

### Preloading data

Default size: `20`GB <br>
To adjust the total size to load

> add `SCAN_COLL_FILLSZ_GB=<size in GB>` to `.env` file

#### Steps

- `docker-compose -f docker-compose.envcheck.yml up -d`
- `docker exec -it alone /bin/bash`
- `python prepare_scancoll.py`

`loadtest.scancoll`(db.coll) is created and loaded with docs up to the given total size(default: `20`GB) <br>
Each doc is `512`B in bson size

---
