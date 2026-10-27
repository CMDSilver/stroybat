import requests
from decimal import Decimal


class APIError(Exception):
    pass


class StroybatAPI:
    def __init__(self, base_url="https://stroybat-api.onrender.com"):
        self.base_url = base_url.rstrip("/")
        self.timeout = 30

    def login(self, username, password):
        response = requests.post(
            f"{self.base_url}/login",
            json={
                "username": username,
                "password": password
            },
            timeout=15
        )

        response.raise_for_status()
        return response.json()

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"

        try:
            response = requests.request(
                method,
                url,
                timeout=self.timeout,
                **kwargs
            )
        except requests.RequestException as error:
            raise APIError(
                "Не удалось подключиться к серверу. "
                "Проверь интернет и доступность API."
            ) from error

        if not response.ok:
            try:
                detail = response.json().get(
                    "detail", response.text
                )
            except (ValueError, AttributeError):
                detail = response.text

            raise APIError(
                f"Ошибка сервера ({response.status_code}): {detail}"
            )

        if response.status_code == 204 or not response.content:
            return None

        try:
            return response.json()
        except ValueError as error:
            raise APIError(
                "Сервер вернул ответ в неизвестном формате."
            ) from error


    def check_connection(self):
        return self._request("GET", "/status")

    def get_users(self):
        return self._request("GET", "/users")

    def create_user(self, username, password):
        data = {
            "full_name": username,
            "username": username,
            "password": password,
            "role_id": 2
        }
        return self._request("POST", "/users", json=data)

    def get_projects(self, search=None, status=None):
        params = {}
        if search:
            params["search"] = search
        if status:
            params["status"] = status

        return self._request("GET", "/projects", params=params)

    def get_project(self, project_id):
        return self._request("GET", f"/projects/{project_id}")

    def create_project(
        self,
        name,
        manager_id,
        description="",
        status="new",
        start_date=None,
        end_date=None
    ):
        data = {
            "name": name,
            "description": description or None,
            "status": status,
            "manager_id": manager_id,
            "start_date": start_date or None,
            "end_date": end_date or None,
        }
        return self._request("POST", "/projects", json=data)

    def update_project(self, project_id, **fields):
        allowed = {
            "name", "description", "status",
            "start_date", "end_date", "manager_id"
        }
        data = {
            key: value
            for key, value in fields.items()
            if key in allowed
        }
        return self._request(
            "PUT", f"/projects/{project_id}", json=data
        )

    def delete_project(self, project_id):
        return self._request("DELETE", f"/projects/{project_id}")

    def get_stages(self, project_id):
        return self._request(
            "GET", f"/projects/{project_id}/stages"
        )

    def create_stage(
        self,
        project_id,
        name,
        description="",
        start_date=None,
        end_date=None,
        status="new",
        sort_order=0
    ):
        data = {
            "project_id": project_id,
            "name": name,
            "description": description or None,
            "start_date": start_date or None,
            "end_date": end_date or None,
            "status": status,
            "sort_order": sort_order,
        }
        return self._request("POST", "/stages", json=data)

    def update_stage(self, stage_id, **fields):
        return self._request(
            "PATCH", f"/stages/{stage_id}", json=fields
        )

    def get_tasks(self, stage_id=None, status=None):
        params = {}
        if stage_id is not None:
            params["stage_id"] = stage_id
        if status is not None:
            params["status"] = status

        return self._request("GET", "/tasks", params=params)

    def create_task(
        self,
        title,
        created_by,
        description="",
        stage_id=None,
        assignee_id=None,
        priority="medium",
        status="new",
        due_date=None
    ):
        data = {
            "title": title,
            "description": description or None,
            "stage_id": stage_id,
            "assignee_id": assignee_id,
            "created_by": created_by,
            "priority": priority,
            "status": status,
            "due_date": due_date or None,
        }
        return self._request("POST", "/tasks", json=data)

    def update_task(self, task_id, **fields):
        return self._request(
            "PATCH", f"/tasks/{task_id}", json=fields
        )

    def delete_task(self, task_id):
        return self._request("DELETE", f"/tasks/{task_id}")

    def get_estimates(self, project_id=None):
        params = {}
        if project_id is not None:
            params["project_id"] = project_id

        return self._request(
            "GET", "/estimates", params=params
        )

    def create_estimate(
        self,
        project_id,
        name,
        created_by,
        description="",
        status="draft"
    ):
        data = {
            "project_id": project_id,
            "name": name,
            "description": description or None,
            "status": status,
            "created_by": created_by,
        }
        return self._request("POST", "/estimates", json=data)

    def get_estimate_items(self, estimate_id):
        return self._request(
            "GET", f"/estimates/{estimate_id}/items"
        )

    def add_estimate_item(
        self,
        estimate_id,
        item_type,
        name,
        unit,
        quantity,
        unit_price,
        description=""
    ):
        data = {
            "item_type": item_type,
            "name": name,
            "description": description or None,
            "unit": unit,
            "quantity": str(Decimal(str(quantity))),
            "unit_price": str(Decimal(str(unit_price))),
        }
        return self._request(
            "POST",
            f"/estimates/{estimate_id}/items",
            json=data
        )

    def get_estimate_total(self, estimate_id):
        return self._request(
            "GET", f"/estimates/{estimate_id}/total"
        )

api = StroybatAPI()
