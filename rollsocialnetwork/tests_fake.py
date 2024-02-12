"""
roll tests fake
"""
from faker import Faker
from faker_e164.providers import E164Provider

fake = Faker()
fake.add_provider(E164Provider)
