import random


class User:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'User({repr(self.name)})'


class SocialGraph:
    def __init__(self):
        self.reset()

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def reset(self):
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The no. of users must be greater than the average no. of friendships.
        """
        # Reset graph
        self.reset()

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        possible_friendships = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        random.shuffle(possible_friendships)

        for i in range(num_users * avg_friendships // 2):
            friendships = possible_friendships[i]
            self.add_friendship(friendships[0], friendships[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # Initialize a queue for breadth first search
        q = []

        # Add a path with the provided user_id to queue
        q.append([user_id])

        # Create dict for visited users
        visited = {}  # Note that this is a dictionary, not a set

        # Create a while loop for traversal while queue is not empty
        while len(q) > 0:

            # Dequeue the first path
            path = q.pop(0)

            # Look at the last value in the path to get the user id
            u_id = path[-1]

            # If user not in visited and if user not initial user...
            if u_id not in visited:
                # Add path to dict -- key = user and value = path
                visited[u_id] = path
                # add all connected users (values in dict) to queue
                for user in self.friendships[u_id]:
                    # make a copy of the current path
                    path_copy = list(path)
                    # append the current user
                    path_copy.append(user)
                    # queue the copy
                    q.append(path_copy)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    users = 1000
    sg.populate_graph(users, 5)
    # print(sg.friendships)
    user = 1
    connections = sg.get_all_social_paths(user)
    print(f"User {user} is connected to {len(connections)/users:.2%}% of other users")

    total = 0
    for k, v in connections.items():
        total += len(v)
    print(f"Avg degrees of separation for {users} users {total/len(connections):.2f}")
