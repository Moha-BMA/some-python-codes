from exa_py import Exa
exa=Exa("YOUR_API_KEY_HERE")
SearchFor=input("what you want to search for? :")
response = exa.search(
  SearchFor,
  num_results=5,
  type='keyword',#neural type is better
  include_domains=['https://www.netflix.com'],
)
for result in response.results:
  print(f'Title: {result.title}')
  print(f'URL: {result.url}')
  print()
 
#Here are some additional ideas on what you could search with the Exa API!
#Wikipedia links
#Coding documentation
#Academic papers
#Tweets
#Research papers
#News and media