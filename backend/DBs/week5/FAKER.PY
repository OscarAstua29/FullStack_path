#This file is just to provide random data for car_rental_t1.py file

from faker import Faker
from faker_vehicle import VehicleProvider

fake = Faker()

fake.add_provider(VehicleProvider)

# data = [
#     (
#         fake.name(),
#         fake.email(),
#         fake.user_name(),
#         fake.password(length=10),
#         fake.date_of_birth(minimum_age=18, maximum_age=80),
#         fake.random_element(elements=("active", "inactive", "suspended"))
#     )
#     for _ in range(50)
# ]

# print(data)


for i in range(10):
    print(fake.vehicle_year(), fake.vehicle_make(), fake.vehicle_model())