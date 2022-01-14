import json
import re
import sys
import gzip
import shutil
import datetime

def decompressTweets(compressedTweetFilePath, decompressedFilePath):
	with gzip.open(compressedTweetFilePath, 'rb') as f_in:
		with open(decompressedFilePath, 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)
	return decompressedFilePath

def importTweets(compressedTweetFilePath, decompressedFilePath):
	if (compressedTweetFilePath != "ignore"):
		decompressTweets(compressedTweetFilePath, decompressedFilePath)
	file = open(decompressedFilePath, 'r')
	dict = {}
	for line in file:
		item = json.loads(line)
		if item["user_id_str"] not in dict:
			dict[item["user_id_str"]] = [item]
		else:
			dict[item["user_id_str"]].append(item)
	return dict

def compareHashTags(tweets, hashtagList):
	results = []
	for tweet in tweets:
		hashTagFinder = re.compile(r"#(\w+)")
		hashtags = hashTagFinder.findall(tweet["text"])

		for hashTag in hashtags:
			hashTag = hashTag.lower()
			if hashTag in hashtagList:
				results.append(hashTag + ", " + tweet['id_str'])
	return results

def processTweets(tweets, hashtagList, nodeFilePath, outputFilePath):
	node_file = nodeFilePath
	node_file = open(node_file)
	outputFile = open(outputFilePath, "w")
	for line in node_file:
		line = line.strip()
		if line in tweets:
			matches = compareHashTags(tweets[line], hashtagList)
			if len(matches) > 0:
				outputFile.write("\n".join(compareHashTags(tweets[line], hashtagList)))
				outputFile.write("\n")
	outputFile.close()


def importHashtags(hashTagFilePath):
	hash_file = hashTagFilePath
	hash_file = open(hash_file)
	hashtagList = {}
	for line in hash_file:
		hashtagList[line.lower().strip()] = 1
	return hashtagList

def main():
	a = datetime.datetime.now()
	sysArgs = sys.argv
	compressedTweetFilePath = sysArgs[1]
	decompressedFilePath = sysArgs[2] 
	nodeFilePath = sysArgs[3]
	hashTagFilePath = sysArgs[4]
	outputFilePath = sysArgs[5]
	tweets = importTweets(compressedTweetFilePath,decompressedFilePath)
	hashtagList = importHashtags(hashTagFilePath)
	processTweets(tweets, hashtagList, nodeFilePath, outputFilePath)
	b = datetime.datetime.now()
	c = b-a
	print(c.total_seconds())

if __name__ == "__main__":
	main()