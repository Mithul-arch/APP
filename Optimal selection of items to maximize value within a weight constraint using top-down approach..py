# Top-Down Approach (Memoization / Recursion + Caching)
def knapsack_top_down(weights, values, capacity):
    """
    Solve 0/1 Knapsack using recursion + memoization (Top-Down DP).
    
    Idea: For each item, we have 2 choices:
      1. Skip the item
      2. Take the item (if it fits in the remaining capacity)
    We try both and take the one that gives max value.
    We cache results so we don't recompute the same subproblem twice.
    """
    n = len(weights)
    memo = {} 

    def solve(index, remaining_capacity):
        if index == n or remaining_capacity == 0:
            return 0

        if (index, remaining_capacity) in memo:
            return memo[(index, remaining_capacity)]

        skip = solve(index + 1, remaining_capacity)

        take = 0
        if weights[index] <= remaining_capacity:
            take = values[index] + solve(index + 1, remaining_capacity - weights[index])

        result = max(skip, take)
        memo[(index, remaining_capacity)] = result
        return result

    return solve(0, capacity)

weights = [1, 3, 4, 5]
values = [1, 4, 5, 7]
capacity = 7

print("Top-Down Result:", knapsack_top_down(weights, values, capacity))