# Org Chart Service (FastAPI + Alembic + Docker + PostgreSQL)

## Quick Start

git clone https://github.com/imcaiofabio/the-biz-conquest-orgchart-service.git  
cd orgchart-service  
cp .env.dev .env  
docker compose up --build  

API docs: http://localhost:8000/docs

## Config

.env.dev:

POSTGRES_USER=postgres  
POSTGRES_PASSWORD=postgres  
POSTGRES_DB=orgchart  
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/orgchart  
DEBUG=true

To run in production:  
- use `.env.prod` with production credentials  
- use Docker Secrets, AWS Secrets Manager, or Vault for secure config  
- override `env_file` in docker-compose or set ENV manually in orchestrator

## Database

- Alembic migrations run on container start  
- To seed org charts:

docker exec -it api python scripts/seed_data.py

## Routes

### Org Chart
POST /orgcharts  
GET /orgcharts  

### Employees
POST /orgcharts/{org_id}/employees  
GET /orgcharts/{org_id}/employees  
GET /orgcharts/{org_id}/employees/{id}  
PUT /orgcharts/{org_id}/employees/{id}  
DELETE /orgcharts/{org_id}/employees/{id}  
GET /orgcharts/{org_id}/employees/{id}/direct_reports  
PUT /orgcharts/{org_id}/employees/{id}/promote  

## Logic

- Deletion reassigns reports to deleted employee's manager  
- CEO cannot be deleted  
- Promotion reassigns the current CEO under the new one

## Performance

GET /orgcharts/1234/employees → ~0.41s  
GET /orgcharts/1234/employees/3/direct_reports → ~0.22s  
Tested with 10k org charts and fast queries using indexed fields

## Notes

- Indexed: org_id, manager_id  
- No pagination, tests or production DB volume yet  
