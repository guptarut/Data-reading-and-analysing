"""Assignment 3: Tweet Analysis"""

from typing import List, Dict, TextIO, Tuple

HASH_SYMBOL = '#'
MENTION_SYMBOL = '@'
URL_START = 'http'

# Order of data in the file
FILE_DATE_INDEX = 0
FILE_LOCATION_INDEX = 1
FILE_SOURCE_INDEX = 2
FILE_FAVOURITE_INDEX = 3
FILE_RETWEET_INDEX = 4

# Order of data in a tweet tuple
TWEET_TEXT_INDEX = 0
TWEET_DATE_INDEX = 1
TWEET_SOURCE_INDEX = 2
TWEET_FAVOURITE_INDEX = 3
TWEET_RETWEET_INDEX = 4

# Helper functions.

def first_alnum_substring(text: str) -> str:
    """Return all alphanumeric characters in text from the beginning up to the
    first non-alphanumeric character, or, if text does not contain any
    non-alphanumeric characters, up to the end of text."

    >>> first_alnum_substring('')
    ''
    >>> first_alnum_substring('IamIamIam')
    'iamiamiam'
    >>> first_alnum_substring('IamIamIam!!')
    'iamiamiam'
    >>> first_alnum_substring('IamIamIam!!andMore')
    'iamiamiam'
    >>> first_alnum_substring('$$$money')
    ''
    """

    index = 0
    while index < len(text) and text[index].isalnum():
        index += 1
    return text[: index].lower()


def clean_word(word: str) -> str:
    """Return all alphanumeric characters from word, in the same order as
    they appear in word, converted to lowercase.

    >>> clean_word('')
    ''
    >>> clean_word('AlreadyClean?')
    'alreadyclean'
    >>> clean_word('very123mes$_sy?')
    'very123messy'
    """

    cleaned_word = ''
    for char in word.lower():
        if char.isalnum():
            cleaned_word = cleaned_word + char
    return cleaned_word


# Required functions

def extract_mentions(text: str) -> List[str]:
    """Return a list of all mentions in text, converted to lowercase, with
    duplicates included and the initial MENTION_SYMBOL removed not including
    the empty strings.

    >>> extract_mentions('Hi @UofT do you like @cats @CATS #meowmeow')
    ['uoft', 'cats', 'cats']
    >>> extract_mentions('@cats are #cute @cats @cat meow @meow')
    ['cats', 'cats', 'cat', 'meow']
    >>> extract_mentions('@many@many @cats$extra @meow?!wow')
    ['many', 'cats', 'meow']
    >>> extract_mentions('No valid mentions @ @#wow @! here?')
    []
    """
    mentions_list = []
    text_list = text.split()

    for word in text_list:
        if word[0] == MENTION_SYMBOL:
            mention = first_alnum_substring(word[1:])
            if (mention != ''):
                mentions_list.append(mention)

    return mentions_list

def extract_hashtags(text: str) -> List[str]:
    """Return a list containing all of the unique hashtags in the text,
    (with duplicates not included) in the order they appear in the text,
    converted to lowercase with the initial HASH_SYMBOL removed not
    including the empty strings.

    >>> extract_hashtags('Hi #UofT do you like #cats #CATS #meowmeow')
    ['uoft', 'cats', 'meowmeow']
    >>> extract_hashtags('#cats are #cute #cats @cat meow #meow')
    ['cats', 'cute', 'meow']
    >>> extract_hashtags('#many #cats$extra #meow?!')
    ['many', 'cats', 'meow']
    >>> extract_hashtags('No valid hashtags #! here?')
    []
    """
    hash_list = []
    text_list = text.split()

    for word in text_list:
        if word[0] == HASH_SYMBOL:
            hash_word = first_alnum_substring(word[1:])
            if (hash_word not in hash_list) and (hash_word != ''):
                hash_list.append(hash_word)

    return hash_list

def count_words(text: str, words_count: Dict[str, int]) -> None:
    """Update the counts of words that are not Hashtags, Mentions, or
    URLs in the given dictionary 'words_count'. If a word is not in words_count yet,
    then it is added with count 1.
    
    >>> words_count1 = {'nick': 1}
    >>> count_words("#UofT Nick Frosst: Google Brain re-searcher by day,"
        " singer @goodkidband by night!. https://t.co/5zi4AAAyfS", words_count1)
    >>> words_count1 == {'nick': 2,'frosst': 1,'google':1,'brain': 1,'researcher':\
        1,'by': 2,'day': 1,'singer': 1,'night': 1}
    True

    >>> words_count2 = {'hello': 1}
    >>> text = '#check!! Th!s_out(* i *) (!_!) @ https://t.co/5zi4AAAyfS'
    >>> count_words(text, words_count2)
    >>> words_count2 == {'hello': 1, 'thsout': 1, 'i': 1}
    True
    """
    text_list = text.split()
    word_list = []

    for word in text_list:
        if (word[0] != HASH_SYMBOL) and (word[0] != MENTION_SYMBOL) and \
           (word[0: 4] != URL_START) and (word != ''):
            cleaned_word = (clean_word(word))
            if (cleaned_word != ''):
                word_list.append(cleaned_word)

    for word in word_list:
        if word not in words_count:
            words_count[word] = 1
        else:
            words_count[word] += 1


def invert_dict(orginal_dict: Dict[str, int]) -> Dict[int, List[str]]:
    """Return an inverted dictionary where values from orginal_dict are
    keys and keys from orginal_dict are values in the inverted dictionary.

    >>> invert_dict({'a': 70, 'b': 89, 'c': 70, 'd': 90, 'e': 89, 'f': 85})
    {70: ['a', 'c'], 89: ['b', 'e'], 90: ['d'], 85: ['f']}

    >>> invert_dict({'a': 70})
    {70: ['a']}

    >>> invert_dict({})
    {}
    """
    inverted_dict = {}
    for key in orginal_dict:
        invert_key = orginal_dict[key]
        if invert_key not in inverted_dict:
            inverted_dict[invert_key] = [key]
        else:
            inverted_dict[invert_key].append(key)

    return inverted_dict

def common_words(words_count: Dict[str, int], threshold: int) -> None:
    """Update the given dictionary 'word_counts' so that it only includes 
    at most N(threshold) most common words. In the case of a tie for the
    Nth most common word, all of the words in the tie and words with count
    less than them are omitted.
    Note: Here N = threshold
    Precondition: threshold != 0 
    
    >>> words_count1 = {'nick': 7,'frosst': 9,'google': 5,'brain': 10,'researcher':\
        8,'by': 2,'day': 3,'singer': 1,'night': 1}
    >>> common_words(words_count1, 5)
    >>> words_count1 == {'nick': 7,'frosst': 9,'google': 5,'brain': 10,\
          'researcher': 8}
    True

    >>> words_count2 = {'nick': 7,'by': 7,'day': 4,'singer': 4,'night': 4}
    >>> common_words(words_count2, 4)
    >>> words_count2 == {'nick': 7, 'by': 7}
    True
    """
    if len(words_count) > threshold:
        inverted_words_count = invert_dict(words_count)
        words_count.clear()

        count_list = []
        for count in inverted_words_count:
            count_list.append(count)
        count_list.sort()
        reversed_count_list = count_list[::-1]
        
        for count in reversed_count_list:
            if (len(inverted_words_count[count]) <= threshold): 
                for word in inverted_words_count[count]:
                    words_count[word] = count
                threshold = threshold - len(inverted_words_count[count])
            else:
                threshold = 0

def format_tweet_list(user_tweets_list: List[List[str]]) -> List[tuple]:
    """Return a formatted_user_tweets_list containing every tweet_list
    in the user_tweets_list formatted to the format outlined in the 'read_tweets'
    function section of the assignment handout.

    >>> user_tweets_list = [['20181108132750,Unknown Location,Twitter for Android,0,5',\
    'RT @_AlecJacobson: @UofTCompSci St. George (Downtown) Campus is hiring in '
    'Computational Geometry for a Tenure Stream Faculty Position. Tell your friends!',\
    '', 'https://t.co/O9Oui82dEA'], ['20181106202405,Toronto Ontario,Twitter for '
    'Android,6,1', 'Congratulations to all our fall graduates! https://t.co/iRXYwYUAKa']]
    >>> format_tweet_list(user_tweets_list)
    [('RT @_AlecJacobson: @UofTCompSci St. George (Downtown) Campus is hiring in'
    ' Computational Geometry for a Tenure Stream Faculty Position. Tell your'
    ' friends!\n\nhttps://t.co/O9Oui82dEA', 20181108132750, 'Twitter for'
    ' Android', 0, 5), ('Congratulations to all our fall graduates!'
    ' https://t.co/iRXYwYUAKa', 20181106202405, 'Twitter for Android',\
    6, 1)]

    >>> user_tweets_list = [['20181109193619,Unknown Location,Twitter Web Client,1,0',\
    'From a family of 12 kids in a Kenyan village, this #UofT grad is working to'
    ' help other women get an education https://t.co/UnUMe9zMn4']]
    >>> format_tweet_list(user_tweets_list)
    [('From a family of 12 kids in a Kenyan village, this #UofT grad is working to'
    ' help other women get an education https://t.co/UnUMe9zMn4', 20181109193619, \
    'Twitter Web Client', 1, 0)]
    """
    formatted_user_tweets_list = []
    for user_tweet in user_tweets_list:
        formatted_user_tweet = []
        tweet_text = ''  
        for text in user_tweet[1:]:
            tweet_text += (text + '\n')
        formatted_user_tweet.append(tweet_text.strip())

        tweet_properties = user_tweet[0].split(',')
        formatted_user_tweet.append(int(tweet_properties[FILE_DATE_INDEX]))
        formatted_user_tweet.append(tweet_properties[FILE_SOURCE_INDEX])
        formatted_user_tweet.append(int(tweet_properties[FILE_FAVOURITE_INDEX]))
        formatted_user_tweet.append(int(tweet_properties[FILE_RETWEET_INDEX]))

        formatted_user_tweets_list.append(tuple(formatted_user_tweet))

    return formatted_user_tweets_list
        
def collect_usernames(tweets_file_list: List[str]) -> List[str]:
    """Return a list containing all the usernames that are in the tweets_file.

    >>> tweets_file_list = ['UofTCompSci:', '20181108132750,Unknown Location,Twitter '
    'for Android,0,5','RT @_AlecJacobson: @UofTCompSci St. George (Downtown) Campus is ' 
    'hiring in Computational Geometry for a Tenure Stream Faculty Position. Tell your '
    'friends!', '', 'https://t.co/O9Oui82dEA', '<<<EOT', '20181106202405,Toronto Ontario,'
    'Twitter for Android,6,1','Congratulations to all our fall graduates! '
    'https://t.co/iRXYwYUAKa','<<<EOT', 'UofTArtSci:', '20181109193619,Unknown'
    ' Location,Twitter Web Client,1,0', 'From a family of 12 kids in a Kenyan village, '
    'this #UofT grad is working to help other women get an education https://t.'
    'co/UnUMe9zMn4', '<<<EOT']
    >>> collect_usernames(tweets_file_list)
    ['UofTCompSci:', 'UofTArtSci:']

    >>> tweets_file_list = ['20181108132750,Unknown Location,Twitter '
    'for Android,0,5','RT @_AlecJacobson: @UofTCompSci St. George (Downtown) Campus is ' 
    'hiring in Computational Geometry for a Tenure Stream Faculty Position. Tell your '
    'friends!', '', 'https://t.co/O9Oui82dEA', '<<<EOT', '20181106202405,Toronto Ontario,'
    'Twitter for Android,6,1','Congratulations to all our fall graduates! '
    'https://t.co/iRXYwYUAKa','<<<EOT']
    >>> collect_usernames(tweets_file_list)
    []
    """
    usernames_list = []
    for data in tweets_file_list:
        data_list = (data.split())
        if (len(data_list) == 1) and (data_list[0][-1] == ':') and \
           (data_list[0][0: len(data_list[0]) - 1].isalnum()):
            usernames_list.append(data)
            
    return usernames_list


def strip_data(tweet_data_list: List[str]) -> List[str]:
    """Return a modified_data_list consisting of striped data by striping
    (data delineated by the trailing whitespace) the data from the tweet_data_list.
    
    >>> tweet_data_list = ['UofTCompSci:\n', '20181108132750, Unknown Location, Twitter'
                           ' for Android, 0, 5\n']
    >>> strip_data(tweet_data_list)
    ['UofTCompSci:', '20181108132750, Unknown Location, Twitter for Android, 0, 5']
    >>> tweet_data_list = ['\n']
    >>> strip_data(tweet_data_list)
    ['']
    """
    modified_data_list = []

    for data in tweet_data_list:
        modified_data_list.append(data.strip())

    return modified_data_list


def read_tweets(tweets_file: TextIO) -> Dict[str, List[tuple]]:
    """Return a dictionary after reading all of the data from the given file and
    formatting it into the dictionary which follows the format outlined in the 
    'read_tweets' function section of the assignment handout.
    """
    tweets_dict = {}
    data_list = tweets_file.readlines()
    modified_data_list = strip_data(data_list)
    usernames_list = collect_usernames(modified_data_list)
    
    for username in usernames_list:
        if username != usernames_list[-1]:
            user_tweets = (modified_data_list[modified_data_list.index(username) + 1:\
                                              modified_data_list.index(usernames_list\
                                               [usernames_list.index(username)+1])])
        else:
            user_tweets = (modified_data_list[modified_data_list.index(username)\
                                              + 1:])
        if user_tweets == []:
            tweets_dict[username[0: len(username) - 1].lower()] = []
        else:    
            modified_user_tweets = []
            num_sentinels = user_tweets.count('<<<EOT')
            for _ in range(num_sentinels):
                tweet_list = []
                while user_tweets[0] != '<<<EOT':
                    tweet_list.append(user_tweets[0])
                    user_tweets.remove(user_tweets[0])
                user_tweets.remove('<<<EOT')
                modified_user_tweets.append(tweet_list)  
    
            tweets_dict[username[0: len(username) - 1].lower()] = \
                                     format_tweet_list(modified_user_tweets) 

    return tweets_dict


def most_popular(tweets_dict: Dict[str, List[tuple]], start_date: int, end_date: int)\
    -> str:
    """Return the username of the Twitter user who was most popular on Twitter
    (maximum sum of the favourite counts and retweet counts) between the two
    dates(inclusive of the start and end dates); otherwise string 'tie' in case
    of a tie or no tweets in the date range.
    Precondition: start_date <= end_date
    
    >>> tweets_dict = {'uoftartsci': [('From a family of 12 kids in a Kenyan '
    'village, this #UofT grad is working to help other women get an education'
    ' https://t.coUnUMe9zMn4', 20181109193619, 'Twitter Web Client', 1, 0)], \
    'uoftcompsci': [('RT @_AlecJacobson: @UofTCompSci St. George (Downtown)'
    ' Campus is hiring in Computational Geometry for a Tenure Stream'
    ' Faculty Position. Tell your friends!\n\nhttps://t.co/O9Oui82dEA',\
    20181108132750, 'Twitter for Android', 0, 5),\
    ('Congratulations to all our fall graduates! https://t.co/iRXYwYUAKa',\
    20181106202405, 'Twitter for Android', 6, 1)]}
    >>> most_popular(tweets_dict, 20181105202405, 20181110193619)
    'uoftcompsci'

    >>> tweets_dict = {'uoftartsci': [('From a family of 12 kids in a Kenyan '
    'village, this #UofT grad is working to help other women get an education'
    ' https://t.coUnUMe9zMn4', 20181109193619, 'Twitter Web Client', 5, 7)], \
    'uoft': [], \
    'uoftcompsci': [('RT @_AlecJacobson: @UofTCompSci St. George (Downtown)'
    ' Campus is hiring in Computational Geometry for a Tenure Stream'
    ' Faculty Position. Tell your friends!\n\nhttps://t.co/O9Oui82dEA',\
    20181108132750, 'Twitter for Android', 0, 5),\
    ('Congratulations to all our fall graduates! https://t.co/iRXYwYUAKa',\
    20181106202405, 'Twitter for Android', 6, 1)]}
    >>> most_popular(tweets_dict, 20181105202405, 20181110193619)
    'tie'
    """
    tweets_count_list = []
    usernames_list = []
    for username in tweets_dict:
        user_tweets_count = 0
        in_range_count = 0

        if tweets_dict[username] != []: 
            for tweet_tuple in tweets_dict[username]:
                if start_date <= tweet_tuple[TWEET_DATE_INDEX] <= end_date:
                    in_range_count += 1
                    user_tweets_count += (tweet_tuple[TWEET_FAVOURITE_INDEX] + \
                                      tweet_tuple[TWEET_RETWEET_INDEX])
        if in_range_count > 0:
            tweets_count_list.append(user_tweets_count)
            usernames_list.append(username)

    if (len(tweets_count_list) == 0) or \
       (tweets_count_list.count(max(tweets_count_list)) > 1):
        return 'tie'
    else:
        return usernames_list[tweets_count_list.index(max(tweets_count_list))]


def extract_original_hashtags(text: str, hash_list: List[str]) -> None:
    """Return a list containing all of the unique original hashtags including the
    initial HASH_SYMBOL in the text, in the order in which they appear in the text
    converted into lowercase not including only the HASH_SYMBOL as a hashtag.
    >>> hash_list = []
    >>> extract_original_hashtags('Hi #UofT do you like #cats #CATS #meowmeow', hash_list)
    >>> hash_list == ['#uoft', '#cats', '#meowmeow']
    True
    >>> hash_list = []
    >>> extract_original_hashtags('##cats are $##cute @cat meow #me4ow', hash_list)
    >>> hash_list == ['#me4ow']
    True
    >>> hash_list = []
    >>> extract_original_hashtags('#MAny #cats$extra #@eow?!', hash_list)
    >>> hash_list == ['#many', '#cats']
    True
    >>> hash_list = []
    >>> extract_original_hashtags('No valid hashtags #! here?', hash_list)
    >>> hash_list == []
    True
    """
    non_hash_list = extract_hashtags(text)

    for word in non_hash_list:
        if (HASH_SYMBOL + word) not in hash_list: 
            hash_list.append(HASH_SYMBOL + word)


def detect_author(tweets_dict: Dict[str, List[tuple]], tweets_text: str) -> str:
    """Return the username of the most likely author of the given tweet_text, based
    on the hashtags they use if all hashtags in the tweets_text are uniquely
    used by that single user only; otherwise, return the string 'unknown'.
    
    >>> tweets_dict = {'uoftartsci': [('From a family of 12 kids in a Kenyan '
    'village, this #UofT grad working to help other women get an education'
    ' https://t.coUnUMe9zMn4', 20181109193619, 'Twitter Web Client',1, 0)], \
    'uoftcompsci': [('RT @_AlecJacobson: @UofTCompSci St. George (Downtown)'
    ' Campus is hiring in Computational Geometry for a Tenure Stream'
    ' Faculty Position. Tell your friends!\n\nhttps://t.co/O9Oui82dEA',\
    20181108132750, 'Twitter for Android',0, 5),\
    ('Congratulations to all our fall graduates! https://t.co/iRXYwYUAKa',\
    20181106202405, 'Twitter for Android', 6, 1),('Today! @nickfrosst is a '
    'panelist at #StartAI! #uoftalumni #UofT https://t.co/k50ea9qKhb'
    ' (via @UofTNews)', 20181103122515, 'Twitter for Android', 5, 0)]}
    >>> detect_author(tweets_dict, 'Today! @nickfrosst is a panelist at'
    ' #StartAI! #uoftalumni #UofT https://t.co/k50ea9qKhb (via @UofTNews)')
    'unknown'

    >>> tweets_dict = {'uoftartsci': [('From a family of 12 kids in a Kenyan '
    'village, this #UofTArtSci #alumini grad working to help other women get an'
    ' education https://t.coUnUMe9zMn4', 20181109193619, \
    'Twitter Web Client', 1, 0)], 'uoft': [], \
    'uoftcompsci': [('RT @_AlecJacobson: @UofTCompSci St. George (Downtown)'
    ' Campus is hiring in Computational Geometry for a Tenure Stream'
    ' Faculty Position. Tell your friends!\n\nhttps://t.co/O9Oui82dEA',\
    20181108132750, 'Twitter for Android', 0, 5),\
    ('Congratulations to all our fall graduates! https://t.co/iRXYwYUAKa',\
    20181106202405, 'Twitter for Android', 6, 1),('Today! @nickfrosst is a '
    'panelist at #StartAI! #uoftalumni #UofT https://t.co/k50ea9qKhb'
    ' (via @UofTNews)', 20181103122515, 'Twitter for Android', 5, 0)]}
    >>> detect_author(tweets_dict, 'Today! @nickfrosst is a panelist at'
    ' #StartAI! #uoftalumni #UofT https://t.co/k50ea9qKhb (via @UofTNews)')
    'uoftcompsci'
    """
    tweets_text_hashtags = []
    usernames_list = []
    match_count_list = []
    extract_original_hashtags(tweets_text, tweets_text_hashtags)

    if len(tweets_text_hashtags) == 0:
        return 'unknown'
    else:
        for username in tweets_dict:
            user_hashtags = []
            match_count = 0

            if tweets_dict[username] != []:
                for tweet_tuple in tweets_dict[username]:    
                    extract_original_hashtags(tweet_tuple[TWEET_TEXT_INDEX],\
                                              user_hashtags)

            for hashtag in tweets_text_hashtags:
                if hashtag in user_hashtags:
                    match_count += 1
            if match_count > 0:
                match_count_list.append(match_count)
                usernames_list.append(username)

        if (len(match_count_list) == 1) and (match_count_list[0] == \
                                         len(tweets_text_hashtags)):
            return usernames_list[0]
        else:
            return 'unknown'

        
if __name__ == '__main__':
    pass
    # If you add any function calls for testing, put them here.
    # Make sure they are indented, so they are within the if statement body.
    # That includes all calls on print, open, and doctest.
