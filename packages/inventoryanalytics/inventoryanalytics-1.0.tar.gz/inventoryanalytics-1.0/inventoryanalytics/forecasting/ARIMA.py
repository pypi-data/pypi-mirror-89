import statsmodels.api as sm, pandas as pd, statistics
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt

N, t = 140, 136
airpass = sm.datasets.get_rdataset("AirPassengers", "datasets")
ts = pd.Series(airpass.data["value"])
ts = ts.astype(float)
model = ARIMA(ts[0:t], order=(0,1,0))
res = model.fit()
print(res.summary())
res.plot_predict(start=ts.index[3], end=ts.index[-1], alpha=0.1)
print("Std residuals: "+str(statistics.stdev(res.resid)))
plt.show()