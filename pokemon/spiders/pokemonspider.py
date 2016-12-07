import scrapy
import urlparse
from scrapy.spiders import Spider
from scrapy.http    import Request
import re
from pokemon.items import PokemonItem

class pokemonspider(Spider) :

	#setting the inital parameters
	name = "pokemon"
	allowed_domains = ["pokemondb.net"]
	start_urls = ["http://pokemondb.net/pokedex/national"]

	#crawledLinks = []

	def parse(self, response) :
		
		#title=response.xpath('//h2/a/@href').extract()[-1]
		links = response.xpath('//a/@href').extract()

		### To store all the links which have crawled till now
		crawledLinks = []

		### To filter out pokemon pages
		linkPattern = re.compile("^\/pokedex\/+")

	#	for link in links :
	#		link = "http://pokemondb.net" + link
	#		yield Request(link,self.parse)

		for link in links :
			### to avoid cyclic loop
			if linkPattern.match(link) and not ("http://pokemondb.net"+link) in crawledLinks :
				link = "http://pokemondb.net" + link
				print(link)
				crawledLinks.append(link)
				yield Request(link,self.parse)

		### Extracting images
		pokemons = response.xpath('//@src').extract()
		for pok in pokemons:
			if (pok.endswith('.jpg')):
				item = PokemonItem()
				item["image_urls"] = [pok]
				yield item

		






