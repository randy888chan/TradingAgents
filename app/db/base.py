# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.user import User  # Adjust if your User model is elsewhere
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# You might need to adjust the import path for User above
# depending on your final User model location relative to this file.
# For now, assuming app.models.user.User is correct.

# If you have multiple model files, you would import them all here, e.g.:
# from app.models.item import Item
# from app.models.order import Order

# This Base will be used by Alembic in env.py to know about your models.
