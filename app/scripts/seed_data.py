
import requests
import random

BASE_URL = "http://localhost:8000"

def create_org(name):
    res = requests.post(f"{BASE_URL}/orgcharts", json={"name": name})
    return res.json()["id"]

def create_employee(org_id, name, title, manager_id=None):
    data = {"name": name, "title": title, "manager_id": manager_id}
    res = requests.post(f"{BASE_URL}/orgcharts/{org_id}/employees", json=data)
    return res.json()["id"]

def seed():
    for i in range(1, 10001):
        org_name = f"Org_{i}"
        org_id = create_org(org_name)
        ceo_id = create_employee(org_id, f"CEO_{i}", "CEO")

        mid_managers = [create_employee(org_id, f"Manager_{i}_{j}", "Manager", ceo_id) for j in range(random.randint(1, 3))]
        for j in range(random.randint(2, 10)):
            manager = random.choice(mid_managers)
            create_employee(org_id, f"Employee_{i}_{j}", "Staff", manager)

        if i % 100 == 0:
            print(f"Seeded {i} org charts")

if __name__ == "__main__":
    seed()
