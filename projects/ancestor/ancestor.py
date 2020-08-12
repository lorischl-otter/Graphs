class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


def earliest_ancestor(ancestors, starting_node):

    # Create adjacency dict
    adjacency = {}

    # Input nodes into dict in reverse order
    # so that we can check upwards for parents
    for a in ancestors:
        # if a[0] not in adjacency:
        #     adjacency[a[0]] = set()
        if a[1] not in adjacency:
            adjacency[a[1]] = set()
        adjacency[a[1]].add(a[0])

    print(adjacency)

    # return negative one if no parents
    if starting_node not in adjacency:
        return -1

    # Using DFS approach
    s = Stack()

    # Add path to starting vertex
    s.push([starting_node])

    # Create set for visited verts
    visited = set()

    # Record path to earliest parent
    earliest = []

    # While queue is not empty:
    while s.size() > 0:

        path = s.pop()

        v = path[-1]

        # Look for last value in path
        if v not in visited:
            visited.add(v)
            if len(path) > len(earliest):
                earliest = list(path)

            # add all parents
            if v in adjacency:
                for parent in adjacency[v]:
                    # add node to path
                    # make a copy of v to append 
                    path_copy = path.copy()
                    path_copy.append(parent)
                    # enqueue the path
                    s.push(path_copy)

    return earliest[-1]
