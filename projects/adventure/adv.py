# from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
# import timeit

# start = timeit.default_timer()

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

"""
Project code begins here.
"""

# Create dictionary of "opposite" directions
opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}


def room_traversal():
    """
    Traverses through rooms based on player's current starting point
    until all rooms have been visited.

    Returns the path taken to visit all rooms, as a list of directions.

    '?' used in created dictionary to indicate unexplored directions
    in a given room.
    """

    # Clear traversal path
    traversal_path.clear()

    # Ensure player is in correct starting place
    player.current_room = world.starting_room

    # Initiate empty dict to store visited rooms
    visited = {}

    # Add starting room to dict
    visited[player.current_room.id] = {}

    # Add exits of starting room to dict
    for exit in player.current_room.get_exits():
        visited[player.current_room.id][exit] = "?"

    # Run while loop until all rooms visited
    while len(visited) < 500:
        # Travel in random directions until a room is reached with no
        # unexplored paths left
        while any(
                v == '?' for k, v in visited[player.current_room.id].items()):
            # Set room variable for code readability
            room = player.current_room

            # Select a random available direction from current room
            directions = [k for k, v in visited[room.id].items() if v == '?']

            # Check to see if any potential direction is a dead end
            dead_end = False
            for d in directions:
                r = room.get_room_in_direction(d)
                if len(r.get_exits()) == 1:
                    dead_end_dir = str(d)
                    dead_end = True

            # If so, move there first
            if dead_end:
                d = str(dead_end_dir)
            # Otherwise, pick a random direction
            else:
                d = random.choice(directions)

            # Add direction to traversal_path
            traversal_path.append(d)

            # Update current room in dictionary
            visited[room.id][d] = room.get_room_in_direction(d).id

            # Travel in selected direction
            player.travel(d)

            # Create variable for new room
            new_room = player.current_room

            if new_room.id not in visited:
                # Create dict with question marks for potential rooms
                visited[new_room.id] = {
                    exit: '?' for exit in new_room.get_exits()}

            # Update new room with a reference to previous room
            visited[new_room.id][opposites[d]] = room.id

        # If all rooms traversed after while loop completes, break loop
        if len(visited) == 500:
            break

        # After player has reached a room with all exits explored,
        # Complete a search to find quickest path to a room w/ unexplored exits
        # And move player down the returned path
        for paths in search(visited, player.current_room.id):
            player.travel(paths[0])
            # Add direction to traversal path
            traversal_path.append(paths[0])

    return traversal_path


def search(visited_rooms, starting_room):
    """
    Breadth-First search coded to find the quickest route to an
    unexplored room, marked by a "?"
    """
    # Initialize queue
    queue = []

    # Add starting room to queue
    queue.append([[starting_room]])

    # Create a set for visited rooms
    bfs_visited = set()

    while len(queue) > 0:
        # Dequeue the first element
        path = queue.pop(0)

        # Grab final room number from path
        room = path[-1][-1]

        if room not in bfs_visited:
            # Check to see if there are any question marks in the room
            if any(v == '?' for k, v in visited_rooms[room].items()):
                # return the path without the original room
                return path[1:]

            # Add room to bfs_visited
            bfs_visited.add(room)

            # Add connected rooms to queue
            for direction, new_room in visited_rooms[room].items():
                # Make a copy of the path
                path_copy = path.copy()
                # Generate path to new_room
                path_copy.append([direction, new_room])
                # Add new path to queue
                queue.append(path_copy)


# Call function multiple times to find the lowest # of moves
best_traversal_path = []

for i in range(1500):
    room_traversal()
    if i == 0:
        best_traversal_path = list(traversal_path)
    elif len(traversal_path) < len(best_traversal_path):
        best_traversal_path = list(traversal_path)

traversal_path = list(best_traversal_path)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, \
        {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

# stop = timeit.default_timer()
# print('Time: ', stop - start)


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
