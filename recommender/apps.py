import os
import pickle

from django.apps import AppConfig

from course import settings


class RecommenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recommender'
    verbose_name = "Recommender System"
    
    def ready(self):
        # Load the trained model when the app is ready
        model_path = os.path.join(settings.BASE_DIR, 'recommender/ml_models/recommender_model.pkl')
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"Recommender model loaded from {model_path}")
        except FileNotFoundError:
            self.model = None
            print(f"Recommender model not found at {model_path}")
