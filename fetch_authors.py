import random
import pandas as pd
from goose import Goose
import newspaper as npp

g = Goose()

output_csv_filename = 'data-from-author-fetch.csv'
input_csv_filename = 'samples-for-author-fetch.csv'
manual_output_csv_filename = 'manual-data-from-author-fetch.csv'
manual_input_csv_filename = 'manual-articles-for-author-fetch.csv'

def lookup_articles_from(input_file, output_file, direct_url=False):
	output_df = pd.DataFrame()
	rows = []

	# ITERATE THROUGH CURATED DATA
	data = pd.read_csv(input_file)
	for index, row in data.iterrows():

		rows = []
		new_list = list(row.values)

		if direct_url==False:
			site_url = row.url
			print site_url
		
			# GET ARTICLES
			site = npp.build(site_url)

		if direct_url==True or len(site.articles) > 0:
			
			if direct_url==False:
				# NEWSPAPER
				article = random.choice(site.articles)
				article.download()
				article.parse()
				story_url = article.url
			else:
				article = npp.Article(row.url)
				article.download()
				article.parse()
				story_url = article.url


			print story_url
			new_list.append(story_url)
			print article.authors
			new_list.append(article.authors)
			print '--\n'

			# GOOSE
			try:
				g_article = g.extract(url=article.url)
			except RuntimeError, re:
				print repr(re)
				new_list.append('Goose ERROR')
			else:	
				# print g_article.authors
				new_list.append(g_article.authors)
			
			print '--\n'

			rows.append(new_list)
			output_df = output_df.append(rows)
			
			# CAPTURE INCREMENTAL RESULTS IN CASE OF FAILURE
			output_df.to_csv(output_file, sep='\t', encoding='utf-8')
		else:
			new_list.append('NO ARTICLES PARSED FROM SITE')
			rows.append(new_list)
			output_df = output_df.append(rows)

			# CAPTURE INCREMENTAL RESULTS IN CASE OF FAILURE
			output_df.to_csv(output_file, sep='\t', encoding='utf-8')

	# WRITE FINAL RESULTS
	output_df.to_csv(output_file, sep='\t', encoding='utf-8')

lookup_articles_from(input_csv_filename, output_csv_filename)
lookup_articles_from(manual_input_csv_filename, manual_output_csv_filename, direct_url=True)
