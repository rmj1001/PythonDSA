import unittest
from src.data_structures.graph import Graph, GraphException, GraphNode
from random import randint

def create_random_graph(nodes: int = 10, edges: bool = False) -> Graph[int, int]:
    graph = Graph()
    rand = lambda: randint(0, 100)

    for num in range(0, nodes, 1):
        graph.insert(num, rand())

    if edges and nodes > 3:
        graph.nodes[0].add_edge(1)
        graph.nodes[0].add_edge(2)
        graph.nodes[1].add_edge(2)
        graph.nodes[2].add_edge(3)
        graph.nodes[2].add_edge(0)
        graph.nodes[3].add_edge(4)

    return graph

class TestGraph(unittest.TestCase):
    def test_insert(self):
        """Test inserting new nodes in the graph"""
        graph: Graph = create_random_graph(10)
        graph2: Graph = create_random_graph(0)

        # Tests insertion, len(), bool(), is_empty(),
        self.assertEqual(len(graph), 10)
        self.assertTrue(graph)

        self.assertFalse(graph2)
        self.assertTrue(graph2.is_empty())

        with self.assertRaises(GraphException):
            graph.insert(0, 10)

    def test_node_equality(self):
        """Check that the values of nodes can be equal"""
        graph: Graph = Graph()

        graph.insert(0, 10)
        graph.insert(1, 10)
        graph.insert(2, 20)

        self.assertEqual(graph.nodes[0], graph.nodes[1])
        self.assertNotEqual(graph.nodes[0], graph.nodes[2])

    def test_unidirectional_edges(self):
        graph: Graph = create_random_graph(10, edges=True)

        # No edges have been made yet
        self.assertEqual(graph.count_edges(), 6)

        # Check number of edges for each node
        self.assertEqual(graph.nodes[0].count_edges(), 2)
        self.assertEqual(graph.nodes[1].count_edges(), 1)
        self.assertEqual(graph.nodes[2].count_edges(), 2)
        self.assertEqual(graph.nodes[3].count_edges(), 1)

        # Check total number of edges
        self.assertEqual(graph.count_edges(), 6)

    def test_remove_node(self):
        graph: Graph = create_random_graph(10, edges=True)

        # Remove node with no edges
        graph.remove_node(1)
        self.assertFalse(graph.node_in_edges(1))

        # Remove node with edges
        graph.remove_node(0)
        self.assertFalse(graph.node_in_edges(0))

    def test_is_bidirectional(self):
        graph: Graph = create_random_graph(10, edges=True)

        # No edges exist
        self.assertFalse(graph.is_bidirectional_edge(3, 0))

        # One edge exists
        self.assertFalse(graph.is_bidirectional_edge(1, 2))

        # Two edges exist
        self.assertTrue(graph.is_bidirectional_edge(0, 2))

    def test_add_bidirectional(self):
        graph: Graph = create_random_graph(10, edges=False)

        graph.add_bidirectional_edge(0, 2)
        self.assertTrue(graph.is_bidirectional_edge(0, 2))

    def test_remove_bidirectional(self):
        graph: Graph = create_random_graph(10, edges=False)

        graph.add_bidirectional_edge(0, 2)
        graph.remove_bidirectional_edge(0, 2)
        self.assertFalse(graph.node_in_edges(0))
        self.assertFalse(graph.node_in_edges(2))

    def test_search(self):
        graph: Graph = Graph()

        graph.insert(0, 10)
        graph.insert(1, 2)
        graph.insert(2, 3)
        graph.insert(3, 4)
        graph.insert(4, 10)

        self.assertEqual(graph.search(2), 1)
        self.assertEqual(graph.search(11), None)
        self.assertEqual(graph.search(10), [0, 4])

    def test_all_edges(self):
        graph: Graph = create_random_graph(10, edges=True)

        edges = [
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 3),
            (2, 0),
            (3, 4)
        ]

        self.assertEqual(graph.all_edges(), edges)

    def test_in_edge(self):
        graph: Graph = create_random_graph(10, edges=True)

        self.assertTrue(graph.node_in_edges(0))
        self.assertFalse(graph.node_in_edges(9))

    def test_bfs(self):
        graph: Graph = Graph()

        # Create nodes
        graph.insert(0, 0)
        graph.insert(1, 10)
        graph.insert(2, 20)
        graph.insert(3, 30)
        graph.insert(4, 40)

        graph.nodes[0].add_edge(1)
        graph.nodes[0].add_edge(2)
        graph.nodes[1].add_edge(2)
        graph.nodes[2].add_edge(3)
        graph.nodes[2].add_edge(0)
        graph.nodes[3].add_edge(4)

        nodes: list[GraphNode] = [node for node in graph.nodes.values()]
        bfs: list[int] = graph.bfs(nodes[0])
        target: list[int] = [0, 10, 20, 30, 40]

        self.assertEqual(bfs, target)

    def test_dfs(self):
        graph: Graph = Graph()

        # Create nodes
        graph.insert(0, 0)
        graph.insert(1, 10)
        graph.insert(2, 20)
        graph.insert(3, 30)
        graph.insert(4, 40)

        graph.nodes[0].add_edge(1)
        graph.nodes[0].add_edge(2)
        graph.nodes[1].add_edge(2)
        graph.nodes[2].add_edge(3)
        graph.nodes[2].add_edge(0)
        graph.nodes[3].add_edge(4)

        nodes: list[GraphNode] = [node for node in graph.nodes.values()]
        dfs: list[int] = graph.dfs(nodes[0])
        target: list[int] = [0, 20, 30, 40, 10]

        self.assertEqual(dfs, target)

    def test_node_methods_and_weights(self):
        graph: Graph[int, int] = Graph()
        graph.insert(0, 100)
        graph.insert(1, 200)

        node0 = graph.nodes[0]
        node0.add_edge(1, weight=5)

        self.assertEqual(len(node0), 1)
        self.assertTrue(node0.is_edge(1))
        self.assertFalse(node0.is_edge(0))
        self.assertEqual(node0.neighbors[1], 5)
        self.assertEqual(node0.all_edges(), [(0, 1)])
        self.assertNotEqual(node0, 100)  # __eq__ with non-GraphNode

        # Duplicate edge raises GraphException
        with self.assertRaises(GraphException):
            node0.add_edge(1)

        # Removing valid and non-existent edges
        node0.remove_edge(1)
        self.assertEqual(len(node0), 0)
        with self.assertRaises(GraphException):
            node0.remove_edge(1)

    def test_exception_paths(self):
        graph: Graph[int, int] = create_random_graph(4, edges=False)

        # Removing non-existent node
        with self.assertRaises(GraphException):
            graph.remove_node(99)

        # Removing bidirectional edge when none exists
        with self.assertRaises(GraphException):
            graph.remove_bidirectional_edge(0, 1)

        # Removing bidirectional edge when only unidirectional exists
        graph.nodes[0].add_edge(1)
        with self.assertRaises(GraphException):
            graph.remove_bidirectional_edge(0, 1)

        # Adding bidirectional edge when unidirectional already exists
        with self.assertRaises(GraphException):
            graph.add_bidirectional_edge(0, 1)

    def test_traversal_edge_cases(self):
        graph: Graph[int, int] = Graph()
        graph.insert(0, 10)
        graph.insert(1, 20)
        graph.insert(2, 30)  # Disconnected component

        # Self-loop + single edge
        graph.nodes[0].add_edge(0)
        graph.nodes[0].add_edge(1)

        # Should not loop infinitely or duplicate 10; should not reach node 2
        self.assertEqual(graph.bfs(graph.nodes[0]), [10, 20])
        self.assertEqual(graph.dfs(graph.nodes[0]), [10, 20])

        # Isolated node traversal
        self.assertEqual(graph.bfs(graph.nodes[2]), [30])
        self.assertEqual(graph.dfs(graph.nodes[2]), [30])

        # Detached/foreign node not in graph
        foreign_node = GraphNode(0, 10)
        self.assertEqual(graph.bfs(foreign_node), [])
        self.assertEqual(graph.dfs(foreign_node), [])

if __name__ == '__main__':
    unittest.main()
