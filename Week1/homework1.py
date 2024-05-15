def better_solution(random_word,dictionary):
        sorted_random_word=sorted(random_word)
        sorted_random_word=''.join(sorted_random_word)

        new_dictionary=[]
        for word in dictionary:
            sorted_word=sorted(word)
            sorted_word=''.join(sorted_word)
            new_dictionary.append((sorted_word,word))
        sorted_new_dictionary=sorted(new_dictionary,key=lambda x:x[0])

        low=0
        high=len(dictionary)-1

        while(low<=high):
            mid=(low+high)//2
            if sorted_random_word==sorted_new_dictionary[mid][0]:
                return sorted_new_dictionary[mid][1]
            elif sorted_random_word<sorted_new_dictionary[mid][0]:
                high=mid-1
            else:
                low=mid+1

        return "None"

def main():
    test1=("statue of liberyt",["tomato","banana","statue of liberty"])
    test2=("",["tomato","banana","statue of liberty"])
    test3=("banana",["nabana,aanann"])
    result1=better_solution(*test1)
    result2=better_solution(*test2)
    result3=better_solution(*test3)
    print(f"Result of test1 is {result1}")
    print(f"Result of test2 is {result2}")
    print(f"Result of test3 is {result3}")


if __name__ == "__main__":
    main()