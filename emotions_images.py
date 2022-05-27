from re import search
from google_images_download import google_images_download 
import sys
import pandas as pd

def get_gimg_urls(search_term, n):
	"""Returns n Google Image urls for a given search term."""
	f = write_gimg_urls(search_term, n)
	urls = parse_gimg_urls(f)
	return urls

def write_gimg_urls(search_term, n):
	"""Write N Google Image urls for a search term S to a text file."""
	f = open('URLS.txt', 'w') 
	orig_stdout, sys.stdout = sys.stdout, f 
	response = google_images_download.googleimagesdownload() 
	arguments = {"keywords":search_term, "limit":n, "print_urls":True}
	orig_stdout.write(search_term + " {}\n".format(n))
	print(search_term, n)
	paths = response.download(arguments) 
	
	sys.stdout = orig_stdout 
	f.close()
	return f

def parse_gimg_urls(urls):
	with open('URLS.txt') as f: content = f.readlines()
	urls = [content[j-1][11:-1] for j in range(len(content)) if content[j][:9] == 'Completed']
	return urls    

def main():

	df = pd.read_csv("emotions.csv")
	emotions = df['emotion'].tolist()
	print(emotions)
	emotion_urls = [get_gimg_urls(e + ' place', 100) for e in emotions]
	print(emotion_urls)
	flat_urls = [link for emo in emotion_urls for link in emo]
	df2 = pd.DataFrame(flat_urls)
	df2.to_csv("emotions_images.csv")
	print()

main()
	