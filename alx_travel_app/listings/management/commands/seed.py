from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        # Optional: clear old data
        Listing.objects.all().delete()

        locations = ['Nairobi', 'Kampala', 'Lagos', 'Accra', 'Johannesburg']
        titles = ['Beach House', 'City Apartment', 'Mountain Cabin', 'Farm Stay', 'Urban Loft']

        for _ in range(10):
            Listing.objects.create(
                title=random.choice(titles),
                description='A wonderful place to stay.',
                price=random.uniform(50, 500),
                location=random.choice(locations)
            )

        self.stdout.write(self.style.SUCCESS('✅ Sample listings created.'))
