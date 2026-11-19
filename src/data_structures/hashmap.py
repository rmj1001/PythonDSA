from collections.abc import Hashable, Iterator, Iterable

type KeyValue[K, V] = tuple[K, V]
type HashList[K, V] = list[KeyValue[K, V]]


class HashMapError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class HashMap[K: Hashable, V]:
    def __init__(self, starting_data: Iterable[KeyValue[K, V]] | None = None, size: int = 100):
        if size <= 0:
            raise HashMapError(f"Size {size} is invalid. Must be greater than 0.")

        self.size: int = size
        self.data: list[HashList[K, V]] = [[] for _ in range(self.size)]
        self._count: int = 0

        if starting_data is not None:
            for k, v in starting_data:
                self.set(k, v)

    def __eq__(self, other: object, /) -> bool:
        """
        Check if two HashMap objects are equal

        ex. HashMap() == HashMap()
        :param other: Other HashMap object
        :return: True if equal, False otherwise
        """
        if not isinstance(other, HashMap):
            return NotImplemented
        if len(self) != len(other):
            return False
        return all(k in other and other[k] == v for k, v in self.entries())

    def __repr__(self) -> str:
        """
        Create a string representation of the HashMap

        ex. str(HashMap)
        :return: str
        """
        if len(self) == 0:
            return 'HashMap{}'

        kvpairs: list[str] = []

        for container in self.data:
            for k, v in container:
                kvpairs.append(f'\t{k}: {v}')

        out = 'HashMap\n{\n' + '\n'.join(kvpairs) + '\n}'

        return out

    def __getitem__(self, key: K) -> V:
        """
        Alias for HashMap.get(key)

        ex. value = HashMap[key]
        :param key: HashMap key
        :return: Value, or raise HashMapError if key doesn't exist
        """
        return self.get(key)

    def __setitem__(self, key: K, value: V) -> None:
        """
        Alias for HashMap.set(key, value)

        ex. HashMap[key] = value
        :param key: HashMap key
        :param value: Value to set
        """
        self.set(key, value)

    def __delitem__(self, key: K) -> None:
        """
        Alias for HashMap.remove(key)

        ex. del HashMap[key]
        :param key: HashMap key
        """
        self.remove(key)

    def __contains__(self, key: K) -> bool:
        """
        Check if a key exists in the HashMap

        ex. exists: bool = key in HashMap()
        :param key: HashMap key
        :return: True if key exists, False otherwise
        """
        try:
            self.get(key)
            return True
        except HashMapError:
            return False

    def __len__(self) -> int:
        """
        Get the number of key/value pairs in the HashMap

        ex. len(HashMap) == 0
        :return: Number of key/value pairs
        """
        return self._count

    def __iter__(self) -> Iterator[K]:
        """
        Iterate over the keys in the HashMap

        ex. iter(HashMap())
        :return: Iterator
        """
        for container in self.data:
            for k, _ in container:
                yield k

    def hash(self, key: K) -> int:
        """
        Get an integer representation of the key from 0 - HashMap.size

        ex. HashMap.hash('Test')
        :param key: The key to hash
        :return: int
        """
        return hash(key) % self.size

    def _get_container(self, key: K) -> HashList[K, V]:
        """
        Get the HashList[K, V] of the key

        ex. HashMap._get_container(key)
        :param key: HashMap key
        :return: HashList[K, V]
        """
        index = self.hash(key)
        return self.data[index]

    def set(self, key: K, value: V) -> None:
        """
        Set a key to a value, or update the value if the key exists

        ex. HashMap.set(key, value)
        :param key: HashMap key
        :param value: Value to set
        """
        container: HashList[K, V] = self._get_container(key)

        for i, (k, v) in enumerate(container):
            if k == key:
                container[i] = (k, value)
                return

        container.append((key, value))
        self._count += 1

    def get(self, key: K, default: V | None = None) -> V:
        """
        Get a value from the HashMap key. If key doesn't exist, return default
        if a default value was provided, else raise HashMapError

        ex. HashMap.get(key, default='Alice')
        :param key: HashMap key
        :param default: Default value to return if key doesn't exist
        :return: Value or default if key doesn't exist
        """
        container: HashList[K, V] = self._get_container(key)

        for k, v in container:
            if k == key:
                return v

        if default is not None:
            return default
        else:
            raise HashMapError(f"Key {key} not found")

    def remove(self, key: K) -> None:
        """
        Remove a key/value pair from the Hashmap based on the key.
        If the key doesn't exist, raise HashMapError.

        ex. HashMap.remove(key)
        :param key: HashMap key
        """
        container: HashList[K, V] = self._get_container(key)

        for i, (k, v) in enumerate(container):
            if k == key:
                del container[i]
                self._count -= 1
                return

        raise HashMapError(f"Key {key} not found")

    def entries(self) -> Iterator[KeyValue[K, V]]:
        """
        Iterate over all key/value pairs in the HashMap

        Ex. for k, v in HashMap.entries()
        :return: Iterator containing all key/value pairs
        """
        for container in self.data:
            for k, v in container:
                yield k, v

    def keys(self) -> Iterator[K]:
        """
        Iterate over all keys in the HashMap

        ex. for k in HashMap.keys()
        :return: Iterator containing all keys
        """
        return iter(self)

    def values(self) -> Iterator[V]:
        """
        Iterate over all values in the HashMap

        ex. for v in HashMap.values()
        :return: Iterator containing all values
        """
        for container in self.data:
            for _, v in container:
                yield v
