from locust import HttpUser, task, between

class MLUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def generate_text(self):
        self.client.post("/generate", json={
            "prompt": "What is 2+2?",
            "max_length": 100,
            "temperature": 0.7,
            "top_p": 0.9
        }) 