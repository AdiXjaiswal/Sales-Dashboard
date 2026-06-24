"""Sales Dashboard source package."""

from .pipeline import data_pipeline, model_pipeline
from .data_loader import load_data
from .feature_engineering import date_time_features
from .kpi import get_kpis

print("src package loaded")

# __all__ = ["data_pipeline"]
