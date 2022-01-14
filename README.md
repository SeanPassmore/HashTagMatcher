Python Hash Tag Parser

To run the Parser using the terminal run the following inside the provided directory:
	python findHashTag.py [compressedTweetPath] [filenameForDecompressedTweets] [nodesPath] [hashtagsPath] [filenameForOutput]
	example: python findHashTag.py tweets.jsonl.gz tweets.jsonl nodes2.txt hashtags2.txt tweetsForNode2.csv

Assumptions:
	Assumed tweets would always be compressed. This seems unlikely but it's good to cover the bases.
	Assumed that it's possible no tweets match certain hashtags
	Assumed that we can fit the list of tweets in memory
	For daily task assumes that tweets are always compressed and have the same file name.
	For daily task assumes that nodes and hashtags always have the same file name.
	For daily task assumes that output file will have the same file names.
	Assumed nodes are correctly formatted
	Assumed hashtags are correctly formatted
	Assumed hashtags wont have non-letter chars

Approach:
	1) Decompress the tweets
	2) Use a dictionary to store tweets where the key is user_id_str and the value is an array of tweets by the user
	3) Load interesting hashtags into a dictionary where key is the hashtag string and the value is 1
	4) Load user id file and read line by line for ids
	5) If user id from the node file is a key in the tweet dictionary compare the content of each tweet
	6) Use Regex to split on matching #+ any number of word characters
	7) If there are results iterate over them
	8) If the result is in the hashtag dictionary create a string with the hashtag and the id_str of the tweet
	9) Write each result to the csv file as we go

Questions:
	Storage Design:
		a) A map table in a database.
			i) Table of Hashtags with hash_id
			ii) Table of Tweets with a tweet_id, tweet_user_id, tweet_date, etc.
			iii) Map Table with matched_tweet_id, matched_hash_id
		b) With a node_id and date filter the tweet table, then join to the map table based on tweet_id = matched_tweet_id (mySQL notation)
	Monitoring:
		With Exception handling and something like Twillow.
		If there's an exception or the process unexpectedly ends on a higher level allow Twillow to send a text.
		Alternatives: A similar integration into Slack, Microsoft Teams, or an Email service.
	API:
		While this depends on how hashtags and node groups are related the simple approach would be as follows:
			1) Use simple CRUD routes
			2) POST Accepts a new user or hashtag designation and an id for users or a text value for hashtags.
				i)If it is already in the DB do nothing.
			3) PUT Accepts a hashtag or user designation, an ID, and a value
				i) This would be used to update a users node group
				ii) This would be used to update a hashtags text value and or node group
			4) DELETE Accepts a user or hashtag designation and an id
			5) GET accepts a user or hashtag designation and filters to get rows from the db
	Scale:
		The solution is still going to be n^2 since the approach relies on nodes * hashtags
		but we take out as much of the searching as possible. Gigabytes a day should be doable 
		with batch processing and multiprocessing combined depending on memory, cpu speed, and cores.

To Do:
	Add tests.(!!!)
	Add multiprocessing for speed at scale.
	Process tweets in batches to avoid using so much memory.
	Add documentation.
	Add exception handling.

