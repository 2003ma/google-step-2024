def count_dictionary_alpha(dictionary):
    with open(dictionary, "r") as f:
        words = f.readlines()

    count_alpha_list = []
    for word in words:
        word = word.strip()  # 改行を削除
        alpha_dict = {}
        for char in word:
            if char in alpha_dict:
                alpha_dict[char] += 1
            else:
                alpha_dict[char] = 1
        list=sorted(alpha_dict.items(),key=lambda x:x[0])
        alpha_dict.clear()
        alpha_dict.update(list)
        count_alpha_list.append((alpha_dict,word))
        
    return count_alpha_list

def calc_score(alpha_dict):
    score_list=[(["a","e","h","i","n","o","r","s","t"],1),(["c","d","l","m","u"],2),(["b","f","g","p","v","w","y"],3),(["j","k","q","x","z"],4)]
    ans=0
    for char in alpha_dict.items():
        if char[0] in score_list[0][0]:
            ans+=char[1]
        elif char[0] in score_list[1][0]:
            ans+=char[1]*2
        elif char[0] in score_list[2][0]:
            ans+=char[1]*3
        else:
            ans+=char[1]*4
    return ans

def better_solution(input_file,output_file):
    dictionary=count_dictionary_alpha("dictionary.txt")
    with open(input_file, "r") as f:
        random_words = f.readlines()

    alpha_count_of_random_word_list=[]
    for random_word in random_words:  #入力単語一語ずつの処理
        alpha_count_of_random_word={}
        random_word = random_word.strip()  # 改行を削除
        for char in random_word:   #含まれているアルファベットを数える
            if char in alpha_count_of_random_word:
                alpha_count_of_random_word[char]+=1
            else:
                alpha_count_of_random_word[char]=1
        list=sorted(alpha_count_of_random_word.items(),key=lambda x:x[0])
        alpha_count_of_random_word.clear()
        alpha_count_of_random_word.update(list)
        alpha_count_of_random_word_list.append((alpha_count_of_random_word,random_word))
    
    anagram_list=[]
    ans_list=[]
    all_score=0
    for alpha_count_of_random_word in alpha_count_of_random_word_list: #ターゲットの文字、クエリ数
        #print(alpha_count_of_random_word)  
        max_score=0
        for dictionary_word in dictionary: #辞書の１単語ずつ考える
            score=0
            anagram_flag=True
            alpha_count_of_dictionary_word=dictionary_word[0]
            for char in alpha_count_of_dictionary_word.items():
                if not char[0] in alpha_count_of_random_word[0]:
                    anagram_flag=False
                    break
                else:
                    same_char_count= alpha_count_of_random_word[0][char[0]]
                    if same_char_count<char[1]:
                        anagram_flag=False
                        break
            if anagram_flag==True:
                score=calc_score(dictionary_word[0])
                anagram_list.append(dictionary_word[1])
            if score>max_score:
                max_score=score 
                max_pair=(max_score,dictionary_word[1])
                
        ans_list.append(max_pair)
        #print(max_pair)
        all_score+=max_pair[0]
    with open(output_file, 'w') as f:
        for d in anagram_list:
            f.write("%s\n" % d)
    
    print(all_score)
        
def main():
    better_solution("small.txt","output_small.txt")
    better_solution("middle.txt","output_middle.txt")
    better_solution("large.txt","output_large.txt")
    

if __name__ == "__main__":
    main()