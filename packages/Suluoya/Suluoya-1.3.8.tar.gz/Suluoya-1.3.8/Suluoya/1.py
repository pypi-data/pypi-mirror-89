import pandas as pd
data = pd.read_clipboard(header=None).values[0][0]
print("从剪切板中得到的array:\n", data)
