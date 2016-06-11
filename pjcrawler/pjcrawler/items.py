# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# url = http://bjn.poderjudicial.gub.uy/BJNPUBLICA/busquedaSimple.seam 

class HojaInsumoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    numero = scrapy.Field()
    sede = scrapy.Field()
    importancia = scrapy.Field() 
    tipo = scrapy.Field()
    fecha = scrapy.Field()
    ficha = scrapy.Field()
    procedimiento = scrapy.Field()
    resumen = scrapy.Field()
    sentencia = scrapy.Field()
