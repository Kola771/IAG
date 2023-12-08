from pathlib import Path

import scrapy

# Voici un spider
# Il permet d'extraire des données d'un site
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        # Ce sont les urls sur lesquels des données seront extraits
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/"
        ]
        # Extraction des données
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        # Extrait le numéro de la page
        page = response.url.split("/")[-2]
        # Le nom du fichier contenant le contenu d'un url
        filename = f"quote-{page}.html"
        # Le contenu d'un url est écrit dans le fichier
        Path(filename).write_bytes(response.body)
        # enregistre un message de journalisation (log) dans le cadre de l'exécution de l'araignée Scrapy. Dans ce cas particulier, la ligne de journalisation informe que le fichier HTML a été sauvegardé avec succès
        self.log(f"Saved file {filename}")