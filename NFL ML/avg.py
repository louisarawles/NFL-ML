def avg(arr):
    print("Calculating average...")
    nums = [x for x in arr if x is not None]
    print(f"nums: {nums}")
    if not nums or len(nums) == 0:
        return 0.0
    return sum(nums) / len(nums)