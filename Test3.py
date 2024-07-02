import scipy 
import numpy as np

start_balance = 5000
end_balance = 1000000

total_time = 10



num_doubles = np.log2(end_balance / start_balance)
double_time = total_time / num_doubles
percent = 72 / double_time

print(num_doubles)
print(percent)