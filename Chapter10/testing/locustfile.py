from locust import HttpUser, task, between

class ListPostUser(HttpUser):
    wait_time = between(1, 3)
    @task
    def post_details(self):
        headers = {
            "Content-Type": "application/json",  # Adjust content type as needed
            # Add other headers if required
        }
        payload = {
            "title": "locustTest"
            # Add more payload data as needed
        }
        response = self.client.post("/posts", json=payload, headers=headers)

