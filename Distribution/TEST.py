import numpy as np
import pandas as pd


arr = np.array([[0.99517764,0.00482236],
                [0.99517764,0.00482236],
                [0.9950119 ,0.0049881 ],
                [0.99517836,0.00482164]])

print(arr)
print(arr[:,:1]*100)
arr=np.round(arr[:,:1],4)
print(arr)

pandas_df = pd.DataFrame(arr, columns=['Probabilité de malveillance'])

print(pandas_df)