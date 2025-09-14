"""
Artificial Intelligence responsible for playing the game of T3!
Implements the alpha-beta-pruning mini-max search algorithm
"""
from dataclasses import *
from typing import *
from t3_state import *
    
def choose(state: "T3State") -> Optional["T3Action"]:
    """
    Main workhorse of the T3Player that makes the optimal decision from the max node
    state given by the parameter to play the game of Tic-Tac-Total.
    
    [!] Remember the tie-breaking criteria! Moves should be selected in order of:
    1. Best utility
    2. Smallest depth of terminal
    3. Earliest move (i.e., lowest col, then row, then move number)
    
    You can view tiebreaking as something of an if-ladder: i.e., only continue to
    evaluate the depth if two candidates have the same utility, only continue to
    evaluate the earliest move if two candidates have the same utility and depth.
    
    Parameters:
        state (T3State):
            The board state from which the agent is making a choice. The board
            state will be either the odds or evens player's turn, and the agent
            should use the T3State methods to simplify its logic to work in
            either case.
    
    Returns:
        Optional[T3Action]:
            If the given state is a terminal (i.e., a win or tie), returns None.
            Otherwise, returns the best T3Action the current player could take
            from the given state by the criteria stated above.
    """

    score, optimal_move = alpha_beta(state, 5, -float("inf"), float("inf"), True)
    return optimal_move if optimal_move is not None else None

def evaluate(state: T3State, is_max: bool, depth: int) -> float:
    '''
    Evaluates the given state and returns a weighted utility.
    
    Parameters:
        state (T3State): 
            The current game state to evaluate.
        is_max (bool): 
            True if maximizing player's turn.
        depth (int): 
            The current depth of the tree.
    
    Returns:
        float: The computed utility value for the state.
    '''
    if is_max:
        return -1 - depth if state.is_win() else 0
    else:
        return 1 + depth if state.is_win() else 0

def alpha_beta(state: T3State, depth:int, alpha: float, beta: float, is_max: bool) -> Tuple[float, Optional[T3Action]]:
    '''
    Alpha-beta pruning minimax algorithm using the skeleton:
    
    function alphabeta(node, α, β, turn)
        if node is a terminal node
            return the utility score of node
        if turn == MAX
            v = -∞
            for each child of node
                v = max(v, alphabeta(child, α, β, MIN))
                α = max(α, v)
                if β ≤ α
                    break
            return v
        else
            v = ∞
            for each child of node
                v = min(v, alphabeta(child, α, β, MAX))
                β = min(β, v)
                if β ≤ α
                    break
            return v
    
    Parameters:
        state (T3State): The current game state.
        depth (int): The maximum depth to search in the game tree.
        alpha (float): The current alpha value for the maximizing player.
        beta (float): The current beta value for the minimizing player.
        is_max (bool): True if it's the maximizing player's turn; False if it's the minimizing player's turn.
    
    Returns:
        Tuple[float, Optional[T3Action]]: A tuple containing the best utility value obtained and the 
        action that leads to that value. If no action is available, returns None for the action.
    '''
    if state.is_win() or state.is_tie() or depth == 0:
        return evaluate(state, is_max, depth), None
    
    if is_max:
        v: float = -float("inf")
        best_action: Optional[T3Action] = None
        for action, child_state in state.get_transitions():
            score, _ = alpha_beta(child_state, depth - 1, alpha, beta, False)
            if score > v:
                v = score
                best_action = action
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v, best_action
    else:
        v: float = float("inf")
        best_action: Optional[T3Action] = None
        for action, child_state in state.get_transitions():
            score, _ = alpha_beta(child_state, depth - 1, alpha, beta, True)
            if score < v:
                v = score
                best_action = action
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v, best_action