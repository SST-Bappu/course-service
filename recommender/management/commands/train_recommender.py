# recommender/management/commands/train_recommender.py

from django.core.management.base import BaseCommand
from course_manager.models import Enrollment, CourseView
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import cross_validate
import pickle
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Train the course recommendation model'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting model training...")

        # Step 1: Extract Data
        enrollments = Enrollment.objects.all().values('user_id', 'course_id')
        enrollments_df = pd.DataFrame(enrollments)
        enrollments_df['rating'] = 1  # Implicit feedback

        views = CourseView.objects.all().values('user_id', 'course_id')
        views_df = pd.DataFrame(views)
        views_df['rating'] = 0.5  # Less weight for views

        # Combine Enrollments and Views
        interactions_df = pd.concat([enrollments_df, views_df], ignore_index=True)

        # Aggregate ratings
        interactions_agg = interactions_df.groupby(['user_id', 'course_id']).agg({'rating': 'max'}).reset_index()

        # Step 2: Prepare Data for Surprise
        reader = Reader(rating_scale=(0.5, 1))
        data = Dataset.load_from_df(interactions_agg[['user_id', 'course_id', 'rating']], reader)

        # Step 3: Choose and Train the Model
        algo = SVD()

        self.stdout.write("Performing cross-validation...")
        cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

        self.stdout.write("Training on the full dataset...")
        trainset = data.build_full_trainset()
        algo.fit(trainset)

        # Step 4: Save the Trained Model
        model_path = os.path.join(settings.BASE_DIR, 'recommender_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(algo, f)

        self.stdout.write(self.style.SUCCESS(f"Model trained and saved to {model_path}"))
