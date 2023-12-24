import json
from faker import Faker
import random
from datetime import datetime

fake = Faker()

dataset = []
# Не смог найти адекватные датасеты в которых можно было бы рассчитать статистику по условию задачи
# Так что создадим свой фейковый датасет про собак (примерно на 30мб)
for i in range(1, 100001):
    dog = {
        "age": random.randint(1, 10),
        "weight_kg": round(random.uniform(5.0, 40.0), 2),
        "height_cm": random.randint(20, 100),
        "vaccinated": random.choice([True, False]),
        "birth_timestamp": fake.date_time_this_decade().isoformat(),
        "is_male": random.choice([True, False]),
        "litter_size": random.randint(1, 12),
        "health_score": round(random.uniform(0.0, 10.0), 2),
        "exercise_hours": round(random.uniform(0.0, 5.0), 2),
        "training_sessions": random.randint(1, 20),
        "feeding_frequency": random.choice(["twice", "thrice", "four times"]),
        "grooming_needs": random.randint(1, 10)
    }
    dataset.append(dog)

# Сохраняем датасет в файл
with open('dog_dataset.json', 'w') as f:
    json.dump(dataset, f, indent=2)
