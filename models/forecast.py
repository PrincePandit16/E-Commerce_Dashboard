import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_percentage_error
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

data_path    = os.path.abspath(os.path.join(current_dir, '..', 'data', 'clean_data.csv'))
plot_path    = os.path.abspath(os.path.join(current_dir, '..', 'data', 'forecast_plot.png'))
comp_path    = os.path.abspath(os.path.join(current_dir, '..', 'data', 'forecast_components.png'))
csv_out_path = os.path.abspath(os.path.join(current_dir, '..', 'data', 'forecast_output.csv'))

df = pd.read_csv(data_path, parse_dates=['InvoiceDate'])

daily = df.groupby(df['InvoiceDate'].dt.date)['Revenue'].sum().reset_index()
daily.columns = ['ds', 'y']
daily['ds'] = pd.to_datetime(daily['ds'])

print(f"Data range: {daily['ds'].min()} to {daily['ds'].max()}")
print(f"Total days: {len(daily)}")

train = daily[:-30]
test  = daily[-30:]

# Fixed: yearly_seasonality='auto' is safe for ~1 year of data
model = Prophet(
    yearly_seasonality='auto',
    weekly_seasonality=True,
    daily_seasonality=False
)
model.fit(train)

future   = model.make_future_dataframe(periods=90)
forecast = model.predict(future)

# Accuracy check
eval_df = test.merge(forecast[['ds', 'yhat']], on='ds', how='inner')
if len(eval_df) > 0:
    mape = mean_absolute_percentage_error(eval_df['y'], eval_df['yhat'])
    print(f"Model MAPE: {mape*100:.2f}%")
    print(f"Model Accuracy: {(1-mape)*100:.2f}%")

# Save forecast plot
fig1 = model.plot(forecast)
plt.title('Sales Forecast — Next 90 Days')
plt.tight_layout()
plt.savefig(plot_path, dpi=150, bbox_inches='tight')
plt.close()  # Fixed: prevents plot overlap
print(f"Forecast plot saved: {plot_path}")

# Save components plot
fig2 = model.plot_components(forecast)
plt.tight_layout()
plt.savefig(comp_path, dpi=150, bbox_inches='tight')
plt.close()  # Fixed: prevents plot overlap
print(f"Components plot saved: {comp_path}")

forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(90).to_csv(
    csv_out_path, index=False)
print("All done! Forecast CSV saved.")