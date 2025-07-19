import pandas as pd
from ydata_profiling import ProfileReport

def profile_data(df):
    profile = ProfileReport(df, minimal=True, explorative=True)
    profile_json = profile.get_description()
    profile_summary = {
        "num_rows": len(df),
        "num_cols": len(df.columns),
        "columns": list(df.columns),
        "missing": df.isnull().sum().to_dict(),
        "types": df.dtypes.apply(str).to_dict()
    }
    # Optionally extract more stats from profile_json
    return profile_json, profile_summary
