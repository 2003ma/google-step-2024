from Week2.submission.homework3_hash import HashTable, Item
import time, sys, random


class Cash:
    def __init__(self, cash_size):
        self.cash_size = cash_size
        self.hash_table = HashTable(self.cash_size)
        self.item_count = 0
        self.head = None
        self.current = None

    def put(self, key, value):
        if self.hash_table.get(key)[1] == True:
            print(value, "already exist")
            return (self.hash_table.get(key)[0], "already exist")

        else:
            if self.item_count == 0:
                self.hash_table.put(key, value)
                new_item = Item(key, value, None)
                self.head = new_item
                self.current = self.head
                self.item_count += 1
                return (value, "first")
            elif 0 < self.item_count < self.cash_size:
                self.hash_table.put(key, value)
                new_item = Item(key, value, None)
                self.current.next = new_item
                self.current = new_item
                self.item_count += 1
                return (value, "only put")
            else:
                delete_key = self.head
                self.head = delete_key.next
                self.hash_table.delete(delete_key.key)
                new_item = Item(key, value, None)
                self.current.next = new_item
                self.current = new_item
                print(delete_key.key)
                return (value, "delete and put")


def functional_test():
    cash = Cash(4)

    print(cash.put("a.com", 1))
    print(cash.put("b.com", 2))
    print(cash.put("c.com", 3))
    print(cash.put("b.com", 2))
    print(cash.put("a.com", 1))
    print(cash.put("c.com", 3))
    print(cash.put("e.com", 4))
    print(cash.put("f.com", 5))
    print(cash.put("h.com", 6))


def performance_test():
    cash = Cash(100)
    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            cash.put(str(rand), str(rand))
        random.seed(iteration)
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))


if __name__ == "__main__":
    functional_test()
    performance_test()
