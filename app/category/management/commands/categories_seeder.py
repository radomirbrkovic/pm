"""
Transaction categories database seeder
"""

from django.core.management.base import BaseCommand
from category.models import Category


class Command(BaseCommand):
    data = [
        {
            'user_id': 1,
            'name': "Salary",
            'type': "income_active"
        },
        {
            'user_id': 1,
            'name': "Bonus",
            'type': "income_active"
        },
        {
            'user_id': 1,
            'name': "Food",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Clothes",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Books",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Utilities",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Other",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Car",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Bank",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Tax",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Accountant",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Pub Quiz - maintaining",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Emergency found",
            'type': "asset"
        },
        {
            'user_id': 1,
            'name': "Found for car",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Found for traveling",
            'type': "liability"
        },
        {
            'user_id': 1,
            'name': "Pub Quiz Found",
            'type': "asset"
        },
    ]

    def handle(self, *args, **options):
        self.stdout.write("Transaction categories database seeder")

        for item in self.data:
            Category.objects.create(**item)

