import random

def simulate_error() -> None:


    if random.randint(1,100) % 2 == 0:  # Simulated condition for failure
        raise Exception("Simulated ingestion failure")