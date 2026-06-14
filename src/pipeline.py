import pandas as pd
from .data_loader import load_data
from . import feature_engineering as fe
from .kpi import get_kpis

def data_pipeline():
    df=load_data('J:/Sales-Dashboard/data/raw_superstore_data.csv')
    fe.date_time_features(df)
    kpis=get_kpis(df)
    return kpis