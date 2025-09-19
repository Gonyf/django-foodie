# your_app/management/commands/generate_test_recipes.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
import random

from faker import Faker

# Import your models - adjust import paths if needed
from recipes.models import Recipe
from foodie_app.models import Category

fake = Faker()


class Command(BaseCommand):
    help = "Generate test categories, users and recipes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--categories", type=int, default=5, help="Number of categories to create."
        )
        parser.add_argument(
            "--users", type=int, default=5, help="Number of users to create."
        )
        parser.add_argument(
            "--recipes", type=int, default=50, help="Number of recipes to create."
        )
        parser.add_argument(
            "--clear", action="store_true", help="Delete existing test data for Recipe/Category created by this script."
        )

    @transaction.atomic
    def handle(self, *args, **options):
        user_temp = get_user_model()
        n_categories = options["categories"]
        n_users = options["users"]
        n_recipes = options["recipes"]
        clear = options["clear"]

        # Optionally clear existing data (be careful in production)
        if clear:
            self.stdout.write("Clearing existing Recipes and Categories created by this script...")
            Recipe.objects.all().delete()
            Category.objects.all().delete()

        # Create categories
        categories = []
        for i in range(n_categories):
            name = fake.word().capitalize()
            cat, created = Category.objects.get_or_create(name=name)
            categories.append(cat)

        # Create users
        users = []
        for i in range(n_users):
            username = f"testuser_{i}_{fake.user_name()}"
            user_temp, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                },
            )
            # If your User model requires a password:
            if created:
                try:
                    user_temp.set_password("password123")
                    user_temp.save()
                except Exception:
                    # Some custom user models may not allow password setting here; ignore if not needed.
                    pass
            users.append(user_temp)

        # helper to build ingredients list text
        def make_ingredients():
            count = random.randint(3, 10)
            lines = []
            for _ in range(count):
                qty = random.choice(
                    [
                        f"{random.randint(1, 3)} cups",
                        f"{random.randint(1, 12)} tbsp",
                        f"{random.randint(1, 8)} tsp",
                        f"{random.randint(1, 6)} pieces",
                        f"{random.randint(1, 2)} lbs",
                    ]
                )
                ingredient = fake.word()
                lines.append(f"{qty} {ingredient}")
            return "\n".join(lines)

        # helper to build directions text
        def make_directions():
            steps = random.randint(2, 8)
            lines = []
            for i in range(1, steps + 1):
                lines.append(f"Step {i}: {fake.sentence(nb_words=random.randint(6, 20))}")
            return "\n\n".join(lines)

        # Create recipes
        created = 0
        for i in range(n_recipes):
            title = fake.sentence(nb_words=random.randint(2, 6)).rstrip(".")
            description = fake.paragraph(nb_sentences=random.randint(1, 3))
            ingredients = make_ingredients()
            directions = make_directions()
            category = random.choice(categories)
            user_temp = random.choice(users + [None]) if users else None  # some recipes with null user

            # Create the recipe
            recipe = Recipe.objects.create(
                name=title[:100],  # adhere to max_length
                description=description,
                ingredients=ingredients,
                directions=directions,
                category=category,
                user=user_temp,
            )

            # Optionally tweak date_added (auto_now_add normally set on save)
            # Example: spread created dates across past 365 days
            try:
                days_ago = random.randint(0, 365)
                dt = timezone.now() - timezone.timedelta(days=days_ago, hours=random.randint(0,23))
                Recipe.objects.filter(pk=recipe.pk).update(date_added=dt)
            except Exception:
                pass

            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} recipes, {len(categories)} categories, {len(users)} users."))
