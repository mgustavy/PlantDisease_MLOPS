from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def predict(self):
        # Assuming we have a test image available
        # You might need to adjust the path or ensure a file exists
        with open("data/train/Healthy/8d30d1e1-bc9f-4ea0-9a34-71209748b589___RS_HL 1962.JPG", "rb") as image:
            self.client.post("/predict", files={"file": image})

    @task(3)
    def health_check(self):
        self.client.get("/")
