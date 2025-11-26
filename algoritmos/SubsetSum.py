import numpy as np

def subset_sum(arr, target):
    dp = np.zeros(target + 1, dtype=bool)
    dp[0] = True

    for x in arr:
        dp[x:] |= dp[:-x]

    return dp[target]