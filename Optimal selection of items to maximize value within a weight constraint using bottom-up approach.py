# Bottom-Up Approach (Tabulation / Iterative DP)
def knapsack_bottom_up(weights, values, capacity):
    """
    Solve 0/1 Knapsack using a DP table (Bottom-Up).
    
    Idea: Build a table dp[i][w] = max value using the first i items
    with weight limit w. We fill it iteratively from smaller subproblems
    up to the full problem — no recursion needed.
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item_weight = weights[i - 1]
        item_value = values[i - 1]

        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]

            if item_weight <= w:
                dp[i][w] = max(dp[i][w], item_value + dp[i - 1][w - item_weight])

    return dp[n][capacity]

weights = [1, 3, 4, 5]
values = [1, 4, 5, 7]
capacity = 7
print("Bottom-Up Result:", knapsack_bottom_up(weights, values, capacity))
