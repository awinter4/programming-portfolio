'''
CMSI 2120 - Homework 1
Author: Andrew Winter

Original Java assignment written by Andrew Forney @forns,
converted to Python by Natalie Lau @nklau.
'''

def get_even_redistribution(amounts: list[int]) -> list[int]:
    
    # Input validation
    if any(i < 0 for i in amounts): # check to see if any index inputted is less than 0 by looping through list/amounts
        raise ValueError("Elements in list must be positive")
    
    number_of_indexes: int = len(amounts) # Quantity of elements in list 

    if number_of_indexes == 0:
        return []

    total_sum: int = sum(amounts) # Sum of elements in list

    # Compute distribution
    even_amount: int = total_sum // number_of_indexes # Case 1: Even amount
    remainder: int = total_sum % number_of_indexes # Case 2: Remainder
    
    # Create new list
    new_list: list[int] = [even_amount] * number_of_indexes
    # Redistribute remainder to largest indexes
    for i in range(1, remainder + 1):
        new_list[-i] += 1

    return new_list

def greedy_changemaker(amount: int) -> list[int]:
    
    # Input validation
    if amount < 0: 
        raise ValueError("Amount must be positive")
    if not isinstance(amount, int):
        raise TypeError("Amount must be an integer")

    coin_denominations: list[int] = [25, 10, 5, 1] # Quarters, dimes, nickels, and pennies
    result: list[int] = []

    # Iterate over each coin denomination 
    for i in coin_denominations: 
        num_coins: int = amount // i # Calculate how many coins of each denomination are needed, starting from biggest to smallest
        result.append(num_coins) # Add number of current denominations used to the result list
        amount %= i # Calculate the remainder after accounting for coins already taken

    return result[::-1] # Return list in reverse order [pennies, nickels, dimes, quarters]