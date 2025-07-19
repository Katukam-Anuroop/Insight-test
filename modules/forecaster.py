from prophet import Prophet
import matplotlib.pyplot as plt
import pandas as pd
import tempfile
from sklearn.metrics import mean_absolute_percentage_error

def forecast_series(df, chart_plan):
    # Heuristic: Look for a date/datetime column and a numeric target
    date_col = None
    target_col = None
    for chart in chart_plan:
        if chart['type'] in ['line', 'area']:
            # Assume first column is datetime, second is value
            if len(chart['columns']) >= 2:
                date_col, target_col = chart['columns'][:2]
            elif len(chart['columns']) == 1:
                date_col = chart['columns'][0]
                # Find next numeric col
                for col in df.select_dtypes(include='number').columns:
                    if col != date_col:
                        target_col = col
                        break
            if date_col and target_col:
                break
    if not date_col or not target_col:
        return None
    # Prophet expects 'ds' and 'y'
    data = df[[date_col, target_col]].dropna()
    data = data.rename(columns={date_col: "ds", target_col: "y"})
    # Try to convert ds to datetime
    data['ds'] = pd.to_datetime(data['ds'])
    m = Prophet()
    m.fit(data)
    future = m.make_future_dataframe(periods=90)
    forecast = m.predict(future)
    # Plot
    fig = m.plot(forecast)
    plot_path = tempfile.mktemp(suffix=".png")
    fig.savefig(plot_path)
    plt.close(fig)
    # Compute MAPE (only on overlapping historical period)
    y_true = data['y'].values
    y_pred = forecast['yhat'][:len(data)].values
    mape = mean_absolute_percentage_error(y_true, y_pred)
    return {
        "forecast_plot": plot_path,
        "mape": round(mape, 3),
        "forecast_summary": forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10).to_dict()
    }
