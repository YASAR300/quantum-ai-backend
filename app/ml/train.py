import os
import pandas as pd
from .preprocess import generate_synthetic, EXPECTED_FEATURES
from .model import train_from_df
from ..config import settings

def load_dataset() -> pd.DataFrame:
    path = settings.DATA_PATH
    if os.path.exists(path):
        df = pd.read_csv(path)

        missing = set(EXPECTED_FEATURES + ["label"]) - set(df.columns)
        if missing:
            raise ValueError(f"Dataset missing columns: {missing}")

        # If only one class present, augment with synthetic to ensure both classes
        if df["label"].nunique() < 2:
            synth = generate_synthetic(n=400)[EXPECTED_FEATURES + ["label"]]
            df = pd.concat([df[EXPECTED_FEATURES + ["label"]], synth], ignore_index=True)
        return df

    # No CSV? Use synthetic
    return generate_synthetic(n=400)

def train_pipeline() -> dict:
    df = load_dataset()
    return train_from_df(df)
