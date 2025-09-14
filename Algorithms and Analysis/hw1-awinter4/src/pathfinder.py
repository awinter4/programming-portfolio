'''
CMSI 2130 - Homework 1
Author: Andrew Winter

Modify only this file as part of your submission, as it will contain all of the logic
necessary for implementing the A* pathfinder that solves the target practice problem.
'''
import queue
from maze_problem import MazeProblem
from dataclasses import *
from typing import *

@dataclass
class SearchTreeNode:
    """
    SearchTreeNodes contain the following attributes to be used in generation of
    the Search tree:

    Attributes:
        priority (int):
            The priority value, combining cost and heuristic. 
        player_loc (tuple[int, int]):
            The player's location in this node.
        action (str):
            The action taken to reach this node from its parent (or empty if the root).
        parent (Optional[SearchTreeNode]):
            The parent node from which this node was generated (or None if the root).
        current_cost (int):
            The cost incurred from start node to this node.
        remaining_targets (Set[Tuple[int, int]]):
            The set of remaining targets yet to shoot. 
    """
    priority: int
    player_loc: tuple[int, int]
    action: str
    parent: Optional["SearchTreeNode"]
    current_cost: int
    remaining_targets: Set[Tuple[int, int]]

    def reconstruct_path(self) -> List[str]:
        """
        Reconstructs the sequence of actions taken to reach a node.
         
        Returns: a list of actions in order. 
        """
        path = []
        current = self

        while current and current.parent:
            path.append(current.action)
            current = current.parent

        return path[::-1]

def manhattan_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> int:
    """
    Calculates the Manhattan Distance between two points

    Parameters: 
        point1 (Tuple[int, int]): x,y coordinates of first location.
        point2 (Tuple[int, int]): x,y coordinates of second location.

    Returns: 
        Int: The Manhattan Distance between both points. 
    """
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def heuristic_distance(player_loc: Tuple[int, int], targets_left: Set[Tuple[int, int]]) -> int:
    """
    The heuristic used is the minimum Manhattan Distance to any remaining target.

    Parameters:
        player_loc (Tuple[int, int]): The current position of the player.
        targets_left (Set[Tuple[int, int]]): The set of remaining target positions. 
    
    Returns: 
        Int: The heurisitic estimate for A* Search
    """
    if not targets_left:
        return 0
    return min(manhattan_distance(player_loc, target) for target in targets_left)

def get_lowest_priority_node(frontier: List[SearchTreeNode]) -> SearchTreeNode:
    """
    Finds and removes the node with the lowest priority from the frontier to ensure frontier expansion.

    Parameters: 
        frontier (List[SearchTreeNode]): The list of nodes in the frontier
    Returns:
        SearchTreeNode: The node with the lowest priority that is removed from the frontier. 
    """
    lowest_index = 0
    for i in range(1, len(frontier)):
        if frontier[i].priority < frontier[lowest_index].priority:
            lowest_index = i
    return frontier.pop(lowest_index)
    
def pathfind(problem: "MazeProblem") -> Optional[list[str]]:
    """
    The main workhorse method of the package that performs A* graph search to find the optimal
    sequence of actions that takes the agent from its initial state and shoots all targets in
    the given MazeProblem's maze, or determines that the problem is unsolvable.

    Parameters:
        problem (MazeProblem):
            The MazeProblem object constructed on the maze that is to be solved or determined
            unsolvable by this method.

    Returns:
        Optional[list[str]]:
            A solution to the problem: a sequence of actions leading from the 
            initial state to the goal (a maze with all targets destroyed). If no such solution is
            possible, returns None.
    """
    
    start_position = problem.get_initial_loc()
    targets = problem.get_initial_targets()

    frontier = [SearchTreeNode(
        priority=heuristic_distance(start_position, targets),
        player_loc=start_position,
        action="",
        parent=None,
        current_cost=0,
        remaining_targets=targets
    )]   

    # For clarification, since this probably looks unclear: 
    # Tuple[int, int] - players position (x, y)
    # Tuple[Tuple[int, int], ...] - a tuple of target positions
    # int - cost associated with reaching that state 
    visited_costs: Dict[Tuple[Tuple[int, int], Tuple[Tuple[int, int], ...]], int] = {}

    while frontier:
        best_index = 0
        for i in range(1, len(frontier)):
            if frontier[i].priority < frontier[best_index].priority:
                best_index = i

        current_node = frontier.pop(best_index)
        current_position = current_node.player_loc
        current_cost = current_node.current_cost
        remaining_targets = current_node.remaining_targets

        if not remaining_targets:
            return current_node.reconstruct_path()

        target_tuple = tuple(sorted(remaining_targets))

        state_key = (current_position, target_tuple)

        if state_key in visited_costs and visited_costs[state_key] <= current_cost:
            continue

        visited_costs[state_key] = current_cost

        possible_moves = problem.get_transitions(current_position, remaining_targets)

        for action, transition in possible_moves.items():
            next_position = transition["next_loc"]
            move_cost = transition["cost"]
            new_targets = remaining_targets - transition["targets_hit"]
            new_total_cost = current_cost + move_cost

            next_node = SearchTreeNode(
                priority=new_total_cost + heuristic_distance(next_position, new_targets),
                player_loc=next_position,
                action=action,
                parent=current_node,
                current_cost=new_total_cost,
                remaining_targets=new_targets
            )

            frontier.append(next_node)
            
    return None

