from homework3_hash import HashTable
import time, sys, random


class DoubleLinkedItem:
    def __init__(self, key, value, next, previous):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next
        self.previous = previous


class Cash:
    def __init__(self, cash_size):
        self.cash_size = cash_size
        self.hash_table = HashTable(self.cash_size)
        self.item_count = 0
        self.head = None
        self.current = None

    def put(self, key, value):
        if self.hash_table.get(key)[1] == True:
            value = self.hash_table.get(key)[0]
            # itemが、移動したい要素の要素のオブジェクト
            item = value[1]
            # 連結リストの先頭の場合
            if item.previous == None:
                item.next.previous = None
                self.head = item.next
                self.current.next = item
                item.previous = self.current
                self.current = item
            # 連結リストの真ん中にある時
            elif item.next != None:
                # 連結リストを消す
                previous = item.previous
                previous.next = item.next
                next = item.next
                next.previous = previous
                # itemをリストの最後尾に加える
                self.current.next = item
                item.previous = self.current
                self.current = item
            return (value[0], "already exist")

        else:
            if self.item_count == 0:
                new_item = DoubleLinkedItem(key, value, None, None)
                self.hash_table.put(key, (value, new_item))
                self.head = new_item
                self.current = self.head
                self.item_count += 1
                return (value, "first")
            elif 0 < self.item_count < self.cash_size:
                new_item = DoubleLinkedItem(key, value, None, None)
                self.hash_table.put(key, (value, new_item))
                self.current.next = new_item
                new_item.previous = self.current
                self.current = new_item
                self.item_count += 1
                return (value, "only put")
            else:
                delete_key = self.head
                self.head = delete_key.next
                self.hash_table.delete(delete_key.key)
                new_item = DoubleLinkedItem(key, value, None, None)
                self.hash_table.put(key, (value, new_item))
                self.current.next = new_item
                self.current = new_item
                return (value, "delete and put")

    def assert_cash(self, keys):
        item = self.head
        for i in range(self.item_count):
            assert item.key == keys[i]
            item = item.next
        return True


def functional_test():
    cash = Cash(4)
    print(cash.put("a.com", 1))
    assert cash.assert_cash(["a.com"]) == True
    print(cash.put("b.com", 2))
    assert cash.assert_cash(["a.com", "b.com"]) == True
    print(cash.put("c.com", 3))
    assert cash.assert_cash(["a.com", "b.com", "c.com"]) == True
    print(cash.put("c.com", 3))
    assert cash.assert_cash(["a.com", "b.com", "c.com"]) == True
    print(cash.put("a.com", 1))
    assert cash.assert_cash(["b.com", "c.com", "a.com"]) == True
    print(cash.put("c.com", 3))
    assert cash.assert_cash(["b.com", "a.com", "c.com"]) == True
    print(cash.put("e.com", 4))
    assert cash.assert_cash(["b.com", "a.com", "c.com", "e.com"]) == True
    print(cash.put("f.com", 5))
    assert cash.assert_cash(["a.com", "c.com", "e.com", "f.com"]) == True
    print(cash.put("h.com", 6))
    assert cash.assert_cash(["c.com", "e.com", "f.com", "h.com"]) == True


if __name__ == "__main__":
    functional_test()
