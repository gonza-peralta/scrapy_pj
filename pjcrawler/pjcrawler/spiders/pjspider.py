'''
Created on May 26, 2016

@author: gonza
'''
# -*- coding: utf-8 -*-
import scrapy
import copy
from datetime import datetime
import urllib
from pjcrawler.items import HojaInsumoItem
from pjcrawler.spiders.constants import SESSION_RE
from pjcrawler.spiders.constants import SESSHASH_RE
from pjcrawler.spiders.constants import POPUP_RE
from pjcrawler.spiders.constants import PAG_RE
from pjcrawler.spiders.constants import STANDAR_ROW
from pjcrawler.spiders.constants import REQUEST_HEADERS
from pjcrawler.spiders.constants import FORMDATA
from pjcrawler.spiders.constants import FORMDATA_POPUP 
from pjcrawler.spiders.constants import FORMDATA_PAG


class PjSpider(scrapy.Spider):
    name = 'pjspider'
    start_urls = ['http://bjn.poderjudicial.gub.uy/BJNPUBLICA/'
                  'busquedaSelectiva.seam']
    url_postpopup = 'http://bjn.poderjudicial.gub.uy/BJNPUBLICA/busquedaSelectiva.seam'
    principal_url = 'http://bjn.poderjudicial.gub.uy/BJNPUBLICA/'\
        'busquedaSelectiva.seam'
    urlprefix = 'http://bjn.poderjudicial.gub.uy'
    url_popup = None
    request_headers = REQUEST_HEADERS
    new_headers = None
    hash_session = None
    formdata = FORMDATA
    formdata_popup = FORMDATA_POPUP 
    formdata_pag = FORMDATA_PAG 

    def start_requests(self):
        for i,url in enumerate(self.start_urls):
            # print(url)
            headers = {"Host": "bjn.poderjudicial.gub.uy",
                       "Connection": "keep-alive",
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                       "Upgrade-Insecure-Requests": "1",
                       "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                       "Accept-Encoding": "gzip, deflate, sdch",
                       "Accept-Language": "en-US,en;q=0.8,es-419;q=0.6,es;q=0.4",
                       }
            yield scrapy.Request(url, callback=self.parse, headers=headers)

    def parse(self, response):
        """
        This is the first page. We must extract cookie info to proceed with
        the next request
        """
        now = datetime.now()
        until = now.strftime("%d/%m/%Y")
        currentmonth = now.strftime("%m/%Y")
        headers = dict(response.headers)
        sessionid = SESSION_RE.findall(headers['Set-Cookie'][0])[0]
        self.hash_session = SESSHASH_RE.findall(sessionid)[0]
        self.new_headers = copy.deepcopy(self.request_headers)
        self.new_headers["Cookie"] = [sessionid]
        # Get form id
        ids = response.xpath("//input[@name='javax.faces.ViewState']"
                             "/@value").extract()
        formid = None
        if len(ids) > 0:
            formid = ids[0]
        if formid:
            self.formdata.append("formBusqueda%3Aj_id20%3Aj_id23%3AfechaDesdeCalInputCurrentDate=" + urllib.quote_plus(currentmonth))
            self.formdata.append("formBusqueda%3Aj_id20%3Aj_id147%3AfechaHastaCalInputDate=" + urllib.quote_plus(until))
            self.formdata.append("formBusqueda%3Aj_id20%3Aj_id147%3AfechaHastaCalInputCurrentDate=" + urllib.quote_plus(currentmonth))
            self.formdata.append("javax.faces.ViewState=" + formid)
            self.formdata_popup.append("javax.faces.ViewState=" + formid)
            self.formdata_pag.append("javax.faces.ViewState=" + formid)
            body = "&".join(self.formdata)
            url_request = self.principal_url + ";jsessionid=" + self.hash_session
            yield scrapy.Request(url_request, callback=self.parse_rows,
                                  method='POST', headers=self.new_headers,
                                  body=body,
                                  dont_filter=True)
        

    def parse_rows(self, response):
        """
        In this function we must parse every row.
        Extract row id and popup url
        For each row we must need to execute a POST and then a GET to the
        popup url
        """
        response.selector.remove_namespaces()
        # Get tr
        tr = response.xpath("//tbody/tr[starts-with(@class, 'rich-table-row')]")
        paginate = False
        if len(tr) > 0:
            paginate = True
        index = 0
        priority = 2*len(tr)
        for sel in tr:
            popup_event = sel.xpath("td[1]/@onclick").extract()
            popup_link = POPUP_RE.findall(popup_event[0])[0]
            self.url_popup = self.urlprefix + popup_link
            popupform = copy.deepcopy(self.formdata_popup)
            popupform.append(STANDAR_ROW.replace('X', str(index)))
            index += 1
            body = "&".join(popupform)
            # return scrapy.Request(self.url_postpopup, callback=self.get_popup,
            yield scrapy.Request(self.url_postpopup, callback=self.get_popup,
                           method='POST', headers=self.new_headers,
                           body=body,
                           dont_filter=True,
                           priority=priority)
            priority -= 1
            yield scrapy.Request(self.url_popup, callback=self.popup_parser,
                              method='GET', headers=self.new_headers,
                              dont_filter=True,
                              priority=priority)
            priority -= 1
        if paginate:
            span_pag = response.xpath("//span[@class='negrita']/text()")[1].extract()
            current, end = PAG_RE.findall(span_pag)[0]
            # print("current " + current)
            # print("end " + end)
            if int(current) < int(end):
                # paginate
                url_request = self.principal_url + ";jsessionid=" + self.hash_session
                body = "&".join(self.formdata_pag)
                yield scrapy.Request(url_request, callback=self.parse_rows,
                                      method='POST', headers=self.new_headers,
                                      body=body,
                                      dont_filter=True,
                                      priority=priority)

    def get_popup(self, response):
        """
        After send popup post, we must proceed to send GET url to parse popup info
        """
        pass
#        return scrapy.Request(self.url_popup, callback=self.popup_parser,
#                              method='GET', headers=self.new_headers,
#                              dont_filter=True)
    
    def popup_parser(self, response):
        """
        Html wich have the info
        """
        resumen = ''.join([''.join(p.xpath('text()').extract()).strip()
                           for p in 
                           response.xpath('//td[@id="j_id107:0:j_id111"]/p')])
        sent = response.xpath('//span[@id="textoSentenciaBox"]')
        sentencia = sent.xpath(".//text()").extract()
        item = HojaInsumoItem()
        item['numero'] = response.xpath('//td[@id="j_id3:0:j_id13"]/text()').extract()[0]
        item['sede'] = response.xpath('//td[@id="j_id3:0:j_id15"]/text()').extract()[0]
        item['importancia'] = response.xpath('//td[@id="j_id3:0:j_id17"]/text()').extract()[0]
        item['tipo'] = response.xpath('//td[@id="j_id3:0:j_id19"]/text()').extract()[0]
        item['fecha'] = response.xpath('//td[@id="j_id21:0:j_id29"]/text()').extract()[0]
        item['ficha'] = response.xpath('//td[@id="j_id21:0:j_id31"]/text()').extract()[0]
        item['procedimiento'] = response.xpath('//td[@id="j_id21:0:j_id33"]/text()').extract()[0]
        # item['resumen'] = resumen
        # item['sentencia'] = sentencia
        return item

        
        
