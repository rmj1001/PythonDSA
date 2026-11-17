from .queue import Queue
from .stack import Stack

type NodeEdge[I] = tuple[I, I]
type Neighbors[I] = dict[I, int]


class GraphException[T](Exception):
    def __init__(self, message: T):
        super().__init__(message)


class GraphNode[I, T]:
    def __init__(self, node_id: I, value: T, neighbors: Neighbors | None = None) -> None:
        self.node_id: I = node_id
        self.value: T = value
        self.neighbors: Neighbors[I] = neighbors if neighbors is not None else {}

    def __len__(self) -> int:
        """
        Alias for GraphNode.count_edges()
        :return: Number of edges
        """
        return self.count_edges()

    def __eq__(self, other: object) -> bool:
        """
        Check if values of two nodes are equal
        :param other: Other node
        :return: True if other object is GraphNode and values are equal, else False
        """
        if not isinstance(other, GraphNode):
            return NotImplemented

        return self.value == other.value

    def count_edges(self):
        """
        Get the number of edges between this node and other nodes
        :return: Number of edges
        """
        return len(self.neighbors)

    def is_edge(self, other_node: I) -> bool:
        """
        Check to see if other node has an edge with this node
        :param other_node: ID of other node
        :return: True if edge exists, else False
        """
        return other_node in self.neighbors

    def add_edge(self, other_node: I, weight: int = 0) -> None:
        """
        Add an edge between this node and another node
        :param other_node: ID of other node
        :param weight: The weight of the edge
        """
        if other_node in self.neighbors:
            raise GraphException(f'Unidirectional edge exists from {self.node_id} to {other_node}.')

        self.neighbors[other_node] = weight

    def remove_edge(self, other_node: I) -> None:
        """
        Remove an edge between this node and another node
        :param other_node: ID of other node
        """
        if other_node not in self.neighbors:
            raise GraphException(f'Unidirectional edge does not exist from {self.node_id} to {other_node}.')

        del self.neighbors[other_node]

    def all_edges(self) -> list[tuple[I, I]]:
        """
        Get a list of all edges for this node, denoted by tuple[node_id, node_id]
        :return: List of edges
        """
        edges: list[tuple[I, I]] = []

        for neighbor in self.neighbors:
            edges.append((self.node_id, neighbor))

        return edges


class Graph[I, T]:
    nodes: dict[I, GraphNode[I, T]]

    def __init__(self) -> None:
        self.nodes = {}

    def __len__(self) -> int:
        """
        Get the number of nodes in the graph
        :return: Number of nodes
        """
        return len(self.nodes)

    def __bool__(self) -> bool:
        """
        Check if the graph contains nodes
        :return:
        """
        return len(self) > 0

    def is_empty(self) -> bool:
        """
        Check if the graph does not have nodes
        :return: True if no nodes exist, else False
        """
        return len(self) == 0

    def count_edges(self) -> int:
        """
        Get the total number of edges in the graph
        :return: Number of edges
        """
        edges: int = 0

        for node in self.nodes.values():
            edges += node.count_edges()

        return edges

    def insert(self, node_id: I, value: T) -> None:
        """
        Insert a node into the graph
        :param node_id: The ID for the new node
        :param value: The node's value
        """
        if node_id in self.nodes:
            raise GraphException(f'Node with id {node_id} already exists.')

        self.nodes[node_id] = GraphNode(node_id, value)

    def remove_node(self, node_id: I) -> None:
        """
        Remove a node from the graph by its id
        :param node_id: The node's id
        """
        if node_id not in self.nodes:
            raise GraphException(f'Node with id {node_id} does not exist.')

        del self.nodes[node_id]

        for node in self.nodes.values():
            try:
                node.remove_edge(node_id)
            except GraphException:
                continue

    def is_bidirectional_edge(self, node_one: I, node_two: I) -> bool:
        """
        Check if edges exist in two directions between two nodes
        :param node_one: The first node's ID
        :param node_two: the second node's ID
        :return: True if two edges exist, else False
        """
        node_one: GraphNode[I, T] = self.nodes[node_one]
        node_two: GraphNode[I, T] = self.nodes[node_two]

        return node_one.is_edge(node_two.node_id) and node_two.is_edge(node_one.node_id)

    def add_bidirectional_edge(self, node_one: I, node_two: I, weight: int = 0) -> None:
        """
        Create two edges between two nodes so that each node connects to the other bidirectionally
        :param node_one: The first node's ID
        :param node_two: The second node's ID
        :param weight: The weight of both edges
        :return:
        """
        node_one: GraphNode[I, T] = self.nodes[node_one]
        node_two: GraphNode[I, T] = self.nodes[node_two]

        node_one.add_edge(node_two.node_id, weight)
        node_two.add_edge(node_one.node_id, weight)

    def remove_bidirectional_edge(self, node_one: I, node_two: I) -> None:
        """
        Remove all edges between two nodes, so that both nodes do not connect to each other
        :param node_one: The first node's ID
        :param node_two: The second node's ID
        """
        if not self.is_bidirectional_edge(node_one, node_two):
            raise GraphException(f'Bidirectional edge does not exist between nodes {node_one} and {node_two}.')

        node_one: GraphNode[I, T] = self.nodes[node_one]
        node_two: GraphNode[I, T] = self.nodes[node_two]

        node_one.remove_edge(node_two.node_id)
        node_two.remove_edge(node_one.node_id)

    def search(self, value: T) -> I | list[I] | None:
        """
        Find ID(s) of nodes whose value matches the given value
        :param value: The value to search for
        :return: ID, list of IDs, or None, depending on how many IDs were found
        """
        nodes: list[I] = []

        for node in self.nodes.values():
            if node.value == value:
                nodes.append(node.node_id)

        if len(nodes) == 0:
            return None
        elif len(nodes) == 1:
            return nodes[0]
        else:
            return nodes

    def all_edges(self) -> list[NodeEdge]:
        """
        Get a list of all edges in the graph, denoted by tuple[node_id, node_id]
        :return: List of edges
        """
        edges: list[NodeEdge] = []

        for node in self.nodes.values():
            edges.extend(node.all_edges())

        return edges

    def node_in_edges(self, node_id: I) -> bool:
        """
        Check to see if a node ID is contained in any edges
        :param node_id: The ID of the node
        :return: True if any edges contain the node ID, False otherwise
        """
        for node_one, node_two in self.all_edges():
            if node_id == node_one or node_id == node_two:
                return True

        return False

    def bfs(self, start_node: GraphNode[I, T]) -> list[T]:
        """
        Search through all nodes connected to a start node
        without repeating nodes, by visiting each child
        node before their descendants

        :param start_node: The starting node
        :returns: List of values from all visited nodes
        """
        if self.nodes.get(start_node.node_id) is not start_node:
            return []

        visited: set[I] = {start_node.node_id}
        results: list[T] = []
        q: Queue[GraphNode[I, T]] = Queue()

        q.enqueue(start_node)

        while not q.is_empty():
            current = q.dequeue()
            results.append(current.value)

            for neighbor_id in current.neighbors.keys():
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    q.enqueue(self.nodes[neighbor_id])

        return results

    def dfs(self, start_node: GraphNode[I, T]) -> list[T]:
        """
        Search through all nodes connected to a start node
        without repeating nodes, by visiting the descendants
        of each node first, before moving to other child nodes

        :param start_node: The starting node
        :returns: List of values from all visited nodes
        """
        if self.nodes.get(start_node.node_id) is not start_node:
            return []

        visited: set[I] = set()
        results: list[T] = []
        aux_stack: Stack[GraphNode[I, T]] = Stack()
        aux_stack.push(start_node)

        while not aux_stack.is_empty():
            current = aux_stack.pop()

            if current.node_id in visited:
                continue

            for c in current.neighbors.keys():
                if c not in visited:
                    aux_stack.push(self.nodes[c])

            visited.add(current.node_id)
            results.append(current.value)

        return results
