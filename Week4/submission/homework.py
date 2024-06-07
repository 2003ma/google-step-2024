import sys
from collections import deque
import copy


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()

    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        start_key = [k for k, v in self.titles.items() if v == start].pop()
        goal_key = [k for k, v in self.titles.items() if v == goal].pop()
        node_list_queue = deque()
        visited = {}
        visited[start_key] = True
        node_list_queue.append((start_key, [start_key]))
        while not len(node_list_queue) == 0:
            node, list = node_list_queue.popleft()
            if node == goal_key:
                list.append(node)
                print(list)
                return list, True
            else:
                for child in self.links[node]:
                    if not child in visited:
                        temp_list = copy.deepcopy(list)
                        temp_list.append(child)
                        visited[child] = True
                        node_list_queue.append((child, temp_list))
        return [], False

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        page_list = list(self.links.keys())
        page_rank_list = {x: 1 for x in page_list}
        prev_page_rank_list = {x: 0 for x in page_list}
        for i in range(1000):
            prev_page_rank_list = page_rank_list.copy()
            # あとで置き換える
            page_rank_list = {x: 0 for x in page_list}
            # 1つずつノードを見て、つながるノードがある時とない時で分ける
            non_exist_connect_node = []
            exist_connect_node = []
            sum_of_exist_connect_node = 0
            sum_of_non_exist_connect_node = 0
            for node, connect_node_list in self.links.items():
                # つながる先のノードが何もない場合
                if len(connect_node_list) == 0:
                    non_exist_connect_node.append(node)
                    sum_of_non_exist_connect_node += prev_page_rank_list[node]
                else:
                    exist_connect_node.append((node, connect_node_list))
                    sum_of_exist_connect_node += prev_page_rank_list[node]

            # 全てのノードに足されるページランク
            all_added_page_rank = (
                sum_of_non_exist_connect_node + sum_of_exist_connect_node * 0.15
            ) / len(page_list)
            page_rank_list = {
                x: page_rank_list.get(x) + all_added_page_rank for x in page_list
            }

            for node, connect_node_list in exist_connect_node:
                # 部分的にたす
                add_page_rank = (
                    prev_page_rank_list[node] * 0.85 / len(connect_node_list)
                )
                for connect_node in connect_node_list:
                    page_rank_list[connect_node] += add_page_rank
            all_difference = 0
            # 全部のノードの誤差が1e-1の時はflag=0で、ループから抜ける
            flag = 0
            for page in page_list:
                page_rank = page_rank_list[page]
                prev_page_rank = prev_page_rank_list[page]
                difference = page_rank - prev_page_rank
                all_difference += difference
                if difference > 1e-1:
                    flag = 1
            if flag == 0:
                break

            print(f"{i+1}回目のループでの誤差の総和は{all_difference}です")

        sorted_page_rank_list = sorted(
            page_rank_list.items(), key=lambda x: x[1], reverse=True
        )
        print(sorted_page_rank_list[0:10])
        return sorted_page_rank_list[0:10][0]

    def find_something_more_interesting(self, start):
        start_key = [k for k, v in self.titles.items() if v == start].pop()
        node_list_queue = deque()
        visited = {}
        visited[start_key] = True
        node_list_queue.append((start_key, [start_key]))
        ans_list = []
        while not len(node_list_queue) == 0:
            node, list = node_list_queue.popleft()

            for child in self.links[node]:
                if not child in visited:
                    temp_list = copy.deepcopy(list)
                    temp_list.append(child)
                    visited[child] = True
                    node_list_queue.append((child, temp_list))
                    ans_list.append(temp_list)

        sorted_lists = sorted(ans_list, key=len, reverse=True)
        print(sorted_lists[0])
        return self.titles[sorted_lists[0][-1]], True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()
    wikipedia.find_something_more_interesting("渋谷")
