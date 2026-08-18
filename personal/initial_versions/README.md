This is the initial version I made last December 25 to 26, 2024.
During these times, I still do not know about `python-chess`

My problems in this version is that I did not take into account the `color of the player` and where the `line` will end is kinda fixed and is not dynamic.
I also did not know about `io.StringIO` back then which makes the directories super chaotic

# Path of Execution
1. `pgn_scraper.py` - update: converted http into https, manually add directory `PGNs`
2. `pgn_game_stripper.py` - manually add directory `PGNs_indiv`
3. `pgn_timestamp_remover.py` update: I adjusted the try and exception 
4. `./PGNs_clean/aMAINChess_lines_frequency.py` update: I adjusted the os.chdir() into os.chdir('./')

this is the working version of my previous attempt to analyze the openings
<br>
if you want to see the unaltered version whereas the scripts are made in that point in time (i.e. Dec 25-26, 2024), then head to commit: 85198119e3609a4eec2d6d80752b1c4bd393e154

# My Documentation

Status: #baby

Tags: [[chess]] [[python]] [[requests]] [[json and dict]]

Aight, I am making this because I saw most games, the positions are similar
And I didn't know what to move after that
I don't have the strongest memory to remember 1,000 games I have played
Maybe even 2,000

I made inaccuracies and even blunders on this stage which made me crushed by
the opponent

# Here's the plan:
> Get the games of my accounts (hevory and Percival120) from an API
> 	This works by having a Python script then it will scrape the API
> 	The API is this api.chess.com/pub/player/${username}/games/${year}/${_month}/pgn
> 	Which is thanks to openingtree and chess-web-api when I dissected their code 
> 	also to ChatGPT and YouTubers who made a walkthrough when I was skimming through JS language
>
> 	Furthermore, it also works by adding the year and month by for loops

> Since the result will be in a whole month form, we need to chunk it per game

> Since the result have timestamps, we need to remove them until we arrive at this:
###### Example PGN:
```
[Event "Live Chess"]
[Site "Chess.com"]
[Date "2024.12.21"]
[Round "?"]
[White "Artem1991Bojar"]
[Black "Percival120"]
[Result "0-1"]
[TimeControl "600"]
[WhiteElo "1327"]
[BlackElo "1256"]
[Termination "Percival120 won by resignation"]
[ECO "B21"]
[EndTime "9:56:36 GMT+0000"]
[Link "https://www.chess.com/game/live/128513542303"]

1. e4 c5 2. f4 Nc6 3. Nf3 e6 4. Bc4 d5 5. exd5 exd5 6. Bb5 Bd7 7. O-O Nf6 8. d3
Be7 9. Bxc6 Bxc6 10. Qe2 O-O 11. Re1 Re8 12. Qd2 Qc7 13. b3 Bd6 14. Ne5 Rad8 15.
Nxc6 bxc6 16. Rxe8+ Rxe8 17. Nc3 Bxf4 18. Qxf4 Re1+ 19. Kf2 Qxf4+ 20. Bxf4 Rxa1
2. a4 d4 22. Ne4 Ra2 23. Nxf6+ gxf6 24. Bb8 a6 25. Ba7 Rxc2+ 26. Kf3 Rc3 27.
Ke4 Rxb3 28. Bxc5 Rb2 29. g3 Rxh2 30. Bxd4 Ra2 31. Bxf6 Rxa4+ 32. Ke5 Ra5+ 33.
Kd6 c5 34. d4 cxd4 35. Bxd4 Rb5 36. Kc6 Rb3 37. Be5 a5 38. Kc5 a4 39. Kc4 Rb7
3. Kc5 a3 41. Kc6 Ra7 42. Kb5 a2 43. Kb6 a1=Q 44. Bxa1 Rxa1 0-1
```

###### .
> After this, we will make the core of the program which is it classifying the frequency of opening lines


###### Let's get into programming!!!!!!!!

# 1. Scraping the API

We need to incorporate for loops and requests
Requests works as curl so let's test curl, but I have no idea how to download from requests module
Well, I guess it's not

We can use webbrowser to speed things up, but we need to make this code dynamic as possible
```
<html>
<head><title>301 Moved Permanently</title></head>
<body>
<center><h1>301 Moved Permanently</h1></center>
<hr><center>nginx</center>
</body>
</html>
```

Troubleshoot: Perhaps, it has something to concern with User-Agent (or maybe not, since 301 is a redirect) \# UPDATE: It has problem with user-agent, because when I use request, it gives 403 error code
# What is 301 response?
The HTTP status code 301, or "301 redirect", indicates that a requested resource has been permanently moved to a new URL

Let's still give it a shot with requests module
Browser still gives it 301 and 204 response

I TOLD YA, IT IS WITH THE USER-AGENT!!!

# How I did troubleshoot the requests?

I get my headers from the Inspect Element > Console > navigator.userAgent
Can also be searched on Google with "What is my user agent?"
[User Agent Switching - Python Web Scraping](https://www.youtube.com/watch?v=90t9WkQbQ2E)
Thanks to this guy ^

# Configure the user-agent

```
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
```


```
print(pgnRequester.request.headers) # shows the headers including user-agent
```

```
pgnRequester = requests.get('http://api.chess.com/pub/player/percival120/games/2024/12/pgn', headers=headers)
```

`print(pgnRequester.text)`
Now, I the contents  are shown but I want it to be a file

# How to download a file?
```
import requests  
res = requests.get('https://automatetheboringstuff.com/files/rj.txt')  
res.raise_for_status()  
playFile = open('RomeoAndJuliet.txt', 'wb')  
for chunk in res.iter_content(100000):  
        playFile.write(chunk)
playFile.close()
```


!!! comment-global: Well, it goes much more easier to chunk or slice the files now since they have specific line numbers to start and end

The first step is almost done! I just need to delete files which have nothing inside them

# 2 Chunking

Done!

How does it work?
I made a program which will read the file in readlines form which will return a list
I made use of slicing and loops
Then I transferred the result to the with open
Finally, the results will be saved on another directory

# 3 Removing timestamps

All the game is in 1 line and that line is in 23 or (line 22 if we are talking about index)
Speaking of index, we can use list and not regular expression to remove the time stamps
Might not be a convenient way if transposed to PGNs from say lichess but let's stick first to list

# How to convert a string into a list?

```
s = "Geeks for Geeks"

# Splits string into words based on space
a = s.split()
print(a)
```

Output:
`['Geeks', 'for', 'Geeks']`

Done!!!
Or maybe not since I only tested one file

I will do it in batch manner by defining a function
Done!

# 4 Main Program

What's the plan?

> Get a sample size

> Make an algorithm for the frequency of line

Sample size should be 10

I think of using slice as one of the component of the algorithm
With detectors for odds and evens, then proceed to change whether in those areas

I want to also incorporate dictionary
But with dynamic key and value

# How to make a dictionary with dynamic keys and value?

```python
# initialize lists for keys and values
keys = ['a', 'b', 'c']
values = [1, 2, 3]

# initialize empty dictionary
dynamic_dict = {}

# dynamically assign key-value pairs using a loop
for i in range(len(keys)):
    dynamic_dict[keys[i]] = values[i]

# print the resulting dictionary
print(dynamic_dict)
```

The pseudo-result will look something like this:

\{\"\['1.', 'e4', 'c5']": 1, "\[...]": 5}
wherein it is
key as stringify line
value as the frequency

The purpose of this is when it encounters the same line as that of the key, it will skip it, saving it  computing power and for it to not be so complicated

!!! global-comment: should have an option for playing for white or black to better correct mistakes
on those individual sides. This gotta be easy!!! Like just if statements for separating and list index

We're on a troubleshooting:
Since, list cannot be a key, we need to join the list
I plan to add a branching method every move
How should I add it though?

Incorporate it in dictionary?

# How to connect list to form a string?
```
a = ['Geeks', 'for', 'Geeks']
res = ' '.join(a)
print(res)
```

So here's my plan again:
I will put a list as key value pair
\[frequency, Branch #]

# How to get the index of a value in list

```
# list of animals
Animals= ["cat", "dog", "tiger"]
# searching positiion of dog
print(Animals.index("dog"))
```

# How to remove element in list by index?
```
original_list = [1, 2, 3, 4, 5]
index_to_remove = 2

del original_list[index_to_remove]
print(original_list)
```

I need to solve a problem, I don't want it to iterate over all my games
I only want to see positions that were played multiple times


My plan:
I will iterate over the dictionary 
Find the one with only 1 frequency
Iterate over the `line_combination_g` and find the right index
then delete the index in line_listified_more so it wouldn't be iterated anymore

Well, it would'nt work since if I delete one, it will affect the others in the list
Not unless if I get their values

Fixed

Now, we need to add more branches or depth since it only is 2 branches
There will come a problem because of possible index error
And slicing does not also come in handy


MY MISTAKE IS I DIDNT USE THE COPY MODULE!!!


# How to deepcopy in Python?

`copy.deepcopy()`

Fixed!

I am in the stage of beautifying the print

Here we gooo!

For the branch purposes
```
_dict_.keys() returns a list of your _dictionary's_ keys. Once you _got_ the list, the -1 index allows you _getting_ the last element of a list.
```

We're almost finished

The plan for beautifying:
> Get the branch number at the end (for the purpose of ending the branch)
> Rank it by frequency

I need to use an algorithm to sort the lines rank

# How to get the key from value?
```
# creating a new dictionary
my_dict ={"java":100, "python":112, "c":11}

# list out keys and values separately
key_list = list(my_dict.keys())
val_list = list(my_dict.values())

# print key with val 100
position = val_list.index(100)
print(key_list[position])
```

I think the ranking is not going to work since there are bunch of 

This is the most challenging part 

I just found a video
[How To Sort A Dictionary By Value (Python Recipes)](https://www.youtube.com/watch?v=OY9AULPtLIU)

```
# To be printed out
dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
```

I just need to make a new dictionary which is temporary

ITS WORKING!!!!!

ITS FINISHED!!!!!

A little fix to make it interactive
But it's done

My next agenda is to separate between white and black so I can analyze my strengths in each areas

Turns out there is a mistake on my code when cleaning the timestamps
It doesn't show white's next move when the game ends