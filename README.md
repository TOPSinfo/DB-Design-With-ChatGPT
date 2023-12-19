# DB-Design-With-ChatGPT
DB Design With ChatGPT

## Prerequisites

- Make sure, **Docker** is installed in your  machine to run this project

## How To Run

**Step-1:** Create .env file from env.txt
```
cp env.txt .env
```

**Step-2:** Update .env variables

**Step-3:** Run `run-dev.sh` file

```
sh run-dev.sh
```

---

>If everything goes well your django application will run on http://localhost:8000 you can configure port, container info and docker config in docker-compose.yml file.

>You can modify dependancies in pyproject.toml file if needed.