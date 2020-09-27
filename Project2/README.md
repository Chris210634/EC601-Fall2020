Set-up
-----------

Create file "config.yaml" that looks like:

search_tweets_api:
  bearer_token: xxxxxxxxxxxxxxxxxx

Configure enviornment variable with Google private key.

In Windows PowerShell:
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\username\Downloads\my-key.json"

Twitter API
-----------

TwitterAPI.py contains test code for Twitter API.

This file contains four experiments:

1. Fetch the 10 most recent tweets from a user. (I used my twitter account as an exmple)

Output:
-----------------------------------------------------
TWEET ID:  1310278386233860097
It's raining cat and dog
-----------------------------------------------------
-----------------------------------------------------
TWEET ID:  1310278034361024519
It's raining cats and dogs!
-----------------------------------------------------
-----------------------------------------------------
TWEET ID:  1310255933985943552
rediculouslylongwordthatnooneisgoingtouse

That's amazzzing!

twitter APiI ROCKS!
-----------------------------------------------------
-----------------------------------------------------
TWEET ID:  1310255744575582214
rediculouslylongwordthatnooneisgoingtouse
-----------------------------------------------------
-----------------------------------------------------
TWEET ID:  1310231452743864321
Overcast skies in Boston today.
-----------------------------------------------------

2. Fetch a tweet by its ID.

Ouput:
-----------------------------------------------------
TWEET ID:  1310231452743864321
Overcast skies in Boston today.
-----------------------------------------------------

3. Get the trending topics in Boston 

Output:
Trending in Boston:
Patriots
#UFC253
Raiders
Catholic
Burkhead
Lebron
Josh Allen
Rams
Wentz
Bears
Haskins
Trubisky
Nick Foles
Daniel Jones

4. Set up a filtered twitter stream that prints out a live stream of tweets that contain the keywords "Patriots Raiders"

Output:
-----------------------------------------------------
TWEET ID:  1310295540731711488
Rex Burkhead with his second rushing TD of the game, this one from five yards away.

#Patriots 20, Raiders 10 with 6:41 to play in the 3rd Quarter. @ABC6
-----------------------------------------------------
-----------------------------------------------------
TWEET ID:  1310295548491173889
Patriots lead the Raiders 20-10
-----------------------------------------------------
-----------------------------------------------------
TWEET ID:  1310295550470881280
@drosssports I swear this Patriots vs Raiders game is interesting cuz whoever wins has a problem with my Chiefs when they vs us in Arrowhead
-----------------------------------------------------
-----------------------------------------------------
TWEET ID:  1310295550454116352
Patriots stick to the ground game in the red zone, and Red Burkhead has his second TD of the game. 

Capitalized on the Raiders missed FG. 

Best I’ve seen Sony Michel run in a while. 

20-10 Patriots. @abc6 #patriots #nevslv #gopats
-----------------------------------------------------


Google Natural Language API
---------------------------

GoogleNlpAPI.py contains test code for Google NLP API.

This file excercises two functionality of Google NLP Library:

1. Calculate overall sentiment of document.
2. Extract keywords (most important words) from the text. 
    Display salience and sentiment of the keywords.

Ouput:

Text: The chicken laid an egg. The geese swim in the lake.
Sentiment: 0.0, 0.699999988079071
====================
         name: chicken
     salience: 0.6225073933601379
    magnitude: 0.0
        score: 0.0
====================
         name: egg
     salience: 0.20607329905033112
    magnitude: 0.0
        score: 0.0
====================
         name: geese
     salience: 0.09726661443710327
    magnitude: 0.10000000149011612
        score: 0.10000000149011612
====================
         name: lake
     salience: 0.07415266335010529
    magnitude: 0.0
        score: 0.0
====================

Text: I hate that dog. He pees all over the house.
Sentiment: -0.6000000238418579, 1.2999999523162842
====================
         name: dog
     salience: 0.7970621585845947
    magnitude: 0.699999988079071
        score: -0.699999988079071
====================
         name: house
     salience: 0.20293782651424408
    magnitude: 0.0
        score: 0.0
====================

Text: My birthday is tomorrow, I am so excited !!!!!
Sentiment: 0.8999999761581421, 0.8999999761581421
====================
         name: birthday
     salience: 1.0
    magnitude: 0.4000000059604645
        score: 0.4000000059604645
====================