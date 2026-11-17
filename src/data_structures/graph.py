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
        return len(self.neighbors.keys())

    def is_edge(self, neighbor_id: I) -> bool:
        """
        Check to see if other node has an edge with this node
        :param neighbor_id: ID of other node
        :return: True if edge exists, else False
        """
        return neighbor_id in self.neighbors.keys()

    def add_edge(self, neighbor_id: I, weight: int = 0) -> None:
        """
        Add an edge between this node and another node
        :param neighbor_id: ID of other node
        :param weight: The weight of the edge
        """
        if self.is_edge(neighbor_id):
            raise GraphException(f'Unidirectional edge exists from {self.node_id} to {neighbor_id}.')

        self.neighbors[neighbor_id] = weight

    def remove_edge(self, neighbor_id: I) -> None:
        """
        Remove an edge between this node and another node
        :param neighbor_id: ID of other node
        """
        if not self.is_edge(neighbor_id):
            raise GraphException(f'Unidirectional edge does not exist from {self.node_id} to {neighbor_id}.')

        del self.neighbors[neighbor_id]

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

    def has_node(self, node_id: I) -> bool:
        """
        Check if a node ID exists in the graph

        :param node_id: The node's ID
        :return: True if node exists, else False
        """
        return node_id in self.nodes.keys()

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
        if self.has_node(node_id):
            raise GraphException(f'Node with id {node_id} already exists.')

        self.nodes[node_id] = GraphNode(node_id, value)

    def remove_node(self, node_id: I) -> None:
        """
        Remove a node from the graph by its id
        :param node_id: The node's id
        """
        if not self.has_node(node_id):
            raise GraphException(f'Node with id {node_id} does not exist.')

        del self.nodes[node_id]

        for node in self.nodes.values():
            try:
                node.remove_edge(node_id)
            except GraphException:
                continue

    def is_edge(self,
                from_node_id: I,
                to_node_id: I,
                bidirectional: bool = False
                ) -> bool:

        if not self.has_node(from_node_id) or not self.has_node(to_node_id):
            return False

        from_node = self.nodes[from_node_id]
        to_node = self.nodes[to_node_id]

        if bidirectional:
            return from_node.is_edge(to_node_id) and to_node.is_edge(from_node_id)
        else:
            return from_node.is_edge(to_node_id)

    def add_edge(self,
                 from_node_id: I,
                 to_node_id: I,
                 weight: int = 0,
                 bidirectional: bool = False
    ) -> None:
        if not self.has_node(from_node_id):
            raise GraphException(f'Node with id {from_node_id} does not exist.')

        if not self.has_node(to_node_id):
            raise GraphException(f'Node with id {to_node_id} does not exist.')

        from_node = self.nodes[from_node_id]
        to_node = self.nodes[to_node_id]

        if not bidirectional and not from_node.is_edge(to_node_id):
            from_node.add_edge(to_node_id, weight)
            return

        if bidirectional and from_node_id == to_node_id:
            raise GraphException('Cannot bidirectional edge with same node')

        if from_node.is_edge(to_node_id) or to_node.is_edge(from_node_id):
            raise GraphException(f'Edge with id {from_node_id} and id {to_node_id} already exists.')

        from_node.add_edge(to_node_id, weight)
        to_node.add_edge(from_node_id, weight)

    def remove_edge(
        self,
        from_node_id: I,
        to_node_id: I,
        bidirectional: bool = False,
    ) -> None:
        if not self.has_node(from_node_id):
            raise GraphException(f'Node with id {from_node_id} does not exist.')

        if not self.has_node(to_node_id):
            raise GraphException(f'Node with id {to_node_id} does not exist.')

        from_node = self.nodes[from_node_id]
        to_node = self.nodes[to_node_id]

        if not from_node.is_edge(to_node_id):
            raise GraphException(f'Unidirectional edge does not exist from {from_node_id} to {to_node_id}.')

        if bidirectional and not to_node.is_edge(from_node_id):
            raise GraphException(f'Unidirectional edge does not exist from {to_node_id} to {from_node_id}.')

        from_node.remove_edge(to_node_id)

        if bidirectional:
            to_node.remove_edge(from_node_id)

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
