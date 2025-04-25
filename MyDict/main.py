class MyDict:
    def __init__(self, size):
        self.__size = size
        self.__load_factor = 0.75
        self.__count = 0
        self.__lst = [[] for _ in range(size)]
        self._index = 0
        self._deep_index = 0

    def __setitem__(self, key, value):
        key_index = self._hash(key)
        deep_lst = self.__lst[key_index]
        for i, (k, _) in enumerate(deep_lst):
            if key == k:
                deep_lst[i] = (key, value)
                return
        deep_lst.append((key, value))
        self.__count += 1
        if (self.__count / self.__size) > self.__load_factor:
            self._rehash()

    def __getitem__(self, key):
        key_index = self._hash(key)
        deep_lst = self.__lst[key_index]
        for (k, v) in deep_lst:
            if k == key:
                return v
        raise KeyError

    def __delitem__(self, key):
        key_index = self._hash(key)
        deep_lst = self.__lst[key_index]
        for i, (k, _) in enumerate(deep_lst):
            if k == key:
                del deep_lst[i]
                self.__count -= 1
                return
        raise KeyError

    def __contains__(self, key):
        key_index = self._hash(key)
        deep_lst = self.__lst[key_index]
        for (k, _) in deep_lst:
            if k == key:
                return True
        raise KeyError

    def __len__(self):
        return self.__count

    def __iter__(self):
        self._index = 0
        self._deep_index = 0
        return self

    def __next__(self):
        while self._index < self.__size:
            deep_lst = self.__lst[self._index]
            if self._deep_index < len(deep_lst):
                key = deep_lst[self._deep_index][0]
                self._deep_index += 1
                return key
            else:
                self._index += 1
                self._deep_index = 0
        raise StopIteration

    def _hash(self, key):
        return hash(key) % self.__size

    def _rehash(self):
        old_lst = self.__lst
        self.__size *= 2
        self.__count = 0
        self.__lst = [[] for _ in range(self.__size)]
        for i in old_lst:
            for (key, value) in i:
                self[key] = value

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        for deep_lst in self.__lst:
            for (k, _) in deep_lst:
                yield k

    def values(self):
        for deep_lst in self.__lst:
            for (_, v) in deep_lst:
                yield v

    def items(self):
        for deep_lst in self.__lst:
            for (k, v) in deep_lst:
                yield k, v


d = MyDict(size=4)


def test_collision():
    old_hash = d._hash

    def new_hash(key):
        return 0

    d._hash = new_hash

    d["abc"] = 100
    d["cba"] = 200

    bucket = d._MyDict__lst[0]
    assert len(bucket) == 2
    assert ("abc", 100) in bucket
    assert ("cba", 200) in bucket

    del d["abc"]
    del d["cba"]

    d._hash = old_hash

    print("Коллизия обработана корректно!")


test_collision()

d['a'] = 10
assert d['a'] == 10

d['a'] = 20
assert d['a'] == 20

assert 'a' in d
assert d.get('a') == 20

del d['a']
assert len(d) == 0

assert d.get('unknown', 99) == 99

for i in range(5):
    d[i] = i

keys = set()
for k in d:
    keys.add(k)

assert keys == set(range(5))

assert set(d.keys()) == set(range(5))
assert set(d.values()) == {i for i in range(5)}
assert set(d.items()) == {(i, i) for i in range(5)}

for i in range(5, 20):
    d[i] = i
assert len(d) == 20

for i in range(20):
    assert d[i] == i