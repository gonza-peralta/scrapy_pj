'''
Created on May 26, 2016

@author: gonza
'''
import scrapy
import re
import copy
from datetime import datetime
import urllib
from pjcrawler.items import HojaInsumoItem
import time

session_re = re.compile("JSESSIONID=.*\d+")
sesshash_re = re.compile("JSESSIONID=\w*~(.+)")
popup_re = re.compile("/BJNPUBLICA/hojaInsumo2.seam\?cid=\d+")
pag_re = re.compile(".*(\d) de (\d+)")
standar_row = "formResultados%3AdataTable%3AX%3AlinkTituloSentencia="\
    "formResultados%3AdataTable%3AX%3AlinkTituloSentencia&"


class PjSpider(scrapy.Spider):
    name = 'pjspider'
    start_urls = ['http://bjn.poderjudicial.gub.uy/BJNPUBLICA/'
                  'busquedaSelectiva.seam']
    url_postpopup = 'http://bjn.poderjudicial.gub.uy/BJNPUBLICA/busquedaSelectiva.seam'
    principal_url = 'http://bjn.poderjudicial.gub.uy/BJNPUBLICA/'\
        'busquedaSelectiva.seam'
    urlprefix = 'http://bjn.poderjudicial.gub.uy'
    url_popup = None
    request_headers = {
                       "Accept": ["*/*"],
                       "Accept-Encoding": ["gzip, deflate"],
                       "Accept-Language": 
                        ["en-US,en;q=0.8,es-419;q=0.6,es;q=0.4"],
                       "Connection": ["keep-alive"],
                       "Content-Type": 
                        ["application/x-www-form-urlencoded; charset=UTF-8"],
                       "Host": ["bjn.poderjudicial.gub.uy"],
                       "Origin": ["http://bjn.poderjudicial.gub.uy"],
                       "Referer": ["http://bjn.poderjudicial.gub.uy/"\
                        "BJNPUBLICA/busquedaSelectiva.seam"],
                       "User-Agent": ["Mozilla/5.0 (X11; Linux x86_64) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/50.0.2661.102 Safari/537.36"]
                       }
    new_headers = None
    hash_session = None
    formdata = ["AJAXREQUEST=_viewRoot",
                "formBusqueda%3Aj_id18=true",
                #"formBusqueda%3Aj_id20%3Aj_id23%3AfechaDesdeCalInputDate=1/1/2002",
                "formBusqueda%3Aj_id20%3Aj_id23%3AfechaDesdeCalInputDate=1%2F06%2F2016",
                
                
                "formBusqueda%3Aj_id20%3Aj_id23%3AfechaDesdeCalInputCurrentDate=06%2F2016", # FECHA ACTUAL
                
                "formBusqueda%3Aj_id20%3AdecorProcedimiento%3AayudanteProc=",
                "formBusqueda%3Aj_id20%3AdecorProcedimiento%3AsuggestAyudante_selection=",
                "formBusqueda%3Aj_id20%3AdecorMateria%3AcbxMateriacomboboxField=AND",
                "formBusqueda%3Aj_id20%3AdecorMateria%3AcbxMateria=AND",
                "formBusqueda%3Aj_id20%3AdecorMateria%3AMateriaBox=",
                "formBusqueda%3Aj_id20%3AdecorMateria%3AsuggestMateria_selection=",
                "formBusqueda%3Aj_id20%3AdecorFirmante%3AcbxFirmantecomboboxField=AND",
                "formBusqueda%3Aj_id20%3AdecorFirmante%3AcbxFirmante=AND",
                "formBusqueda%3Aj_id20%3AdecorFirmante%3AFirmanteBox=",
                "formBusqueda%3Aj_id20%3AdecorFirmante%3AsuggestFirmante_selection=",
                "formBusqueda%3Aj_id20%3AdecorDiscorde%3Aj_id94comboboxField=AND",
                "formBusqueda%3Aj_id20%3AdecorDiscorde%3Aj_id94=AND",
                "formBusqueda%3Aj_id20%3AdecorDiscorde%3ADiscordeBox=",
                "formBusqueda%3Aj_id20%3AdecorDiscorde%3AsuggestDiscorde_selection=",
                "formBusqueda%3Aj_id20%3Aj_id105%3AtodosLosTipos=on",
                "formBusqueda%3Aj_id20%3Aj_id120%3AcajaQuery=",
                
                
                "formBusqueda%3Aj_id20%3Aj_id147%3AfechaHastaCalInputDate=9%2F06%2F2016",
                "formBusqueda%3Aj_id20%3Aj_id147%3AfechaHastaCalInputCurrentDate=06%2F2016",
                
                
                "formBusqueda%3Aj_id20%3Aj_id160%3AayudanteResumen=",
                "formBusqueda%3Aj_id20%3AdecorRedactor%3AcbxRedactorcomboboxField=AND",
                "formBusqueda%3Aj_id20%3AdecorRedactor%3AcbxRedactor=AND",
                "formBusqueda%3Aj_id20%3AdecorRedactor%3ARedactorBox=",
                "formBusqueda%3Aj_id20%3AdecorRedactor%3AsuggestRedactor_selection=",
                "formBusqueda%3Aj_id20%3AdecorNumero%3AayudanteNumero=",
                "formBusqueda%3Aj_id20%3AdecorImportancia%3AtodasLasImportancias=on",
                
                #"formBusqueda%3Aj_id20%3Aj_id223%3AcantPagcomboboxField%3A200", # PROBAR CON NUMERO GRANDE
                #"formBusqueda%3Aj_id20%3Aj_id223%3AcantPag%3A200", # PROBAR CON NUMERO GRANDE
                "formBusqueda%3Aj_id20%3Aj_id223%3AcantPagcomboboxField=10", # PROBAR CON NUMERO GRANDE
                "formBusqueda%3Aj_id20%3Aj_id223%3AcantPag=10", # PROBAR CON NUMERO GRANDE
                
                "formBusqueda%3Aj_id20%3Aj_id240%3Aj_id248=RELEVANCIA",
                "formBusqueda=formBusqueda=",
                "autoScroll=",
                
                "javax.faces.ViewState=j_id1", #--- SALE DEL faces.ViewState
                
                "formBusqueda%3Aj_id20%3ASearch=formBusqueda%3Aj_id20%3ASearch=",
                "AJAX%3AEVENTS_COUNT=1&"]
    formdata_popup = ["AJAXREQUEST=_viewRoot",
                      "formResultados=formResultados",
                      "autoScroll=",
                      # "javax.faces.ViewState=j_id1",
                      # "formResultados%3AdataTable%3A0%3AlinkTituloSentencia="\
                      # "formResultados%3AdataTable%3A0%3AlinkTituloSentencia&",
                      "AJAX%3AEVENTS_COUNT=1"]
    formdata_pag = ["AJAXREQUEST=_viewRoot",
                    "formResultados=formResultados",
                    "autoScroll=",
                    #"javax.faces.ViewState=j_id2",
                    "formResultados%3AsigLink=formResultados%3AsigLink&",
                    "AJAX%3AEVENTS_COUNT=1"]

    def start_requests(self):
        for i,url in enumerate(self.start_urls):
            # log.msg(url, level=log.INFO)
            print(url)
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
#         with open('first_req.html', 'w') as f:
#             f.write(response.body)
        now = datetime.now()
        until = now.strftime("%d/%m/%Y")
        currentmonth = now.strftime("%m/%Y")
        headers = dict(response.headers)
        sessionid = session_re.findall(headers['Set-Cookie'][0])[0]
        self.hash_session = sesshash_re.findall(sessionid)[0]
        self.new_headers = copy.deepcopy(self.request_headers)
        self.new_headers["Cookie"] = [sessionid]
        # Get form id
        ids = response.xpath("//input[@name='javax.faces.ViewState']"
                             "/@value").extract()
        formid = None
        if len(ids) > 0:
            formid = ids[0]
        if formid:
            self.formdata.append("formBusqueda%3Aj_id20%3Aj_id23%3AfechaDesdeCalInputCurrentDate=" + urllib.quote_plus(until))
            self.formdata.append("formBusqueda%3Aj_id20%3Aj_id147%3AfechaHastaCalInputDate:" + urllib.quote_plus(until))
            self.formdata.append("formBusqueda%3Aj_id20%3Aj_id147%3AfechaHastaCalInputCurrentDate:" + urllib.quote_plus(currentmonth))
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
#         with open('second_req.html', 'w') as f:
#             f.write(response.body)
        response.selector.remove_namespaces()
        # Get tr
        tr = response.xpath("//tbody/tr[starts-with(@class, 'rich-table-row')]")
        paginate = False
        if len(tr) > 0:
            paginate = True
        index = 0
        for sel in tr:
            time.sleep(2)
            popup_event = sel.xpath("td[1]/@onclick").extract()
            popup_link = popup_re.findall(popup_event[0])[0]
            self.url_popup = self.urlprefix + popup_link
            popupform = copy.deepcopy(self.formdata_popup)
            popupform.append(standar_row.replace('X', str(index)))
            index += 1
            body = "&".join(popupform)
            # return scrapy.Request(self.url_postpopup, callback=self.get_popup,
            yield scrapy.Request(self.url_postpopup, callback=self.get_popup,
                           method='POST', headers=self.new_headers,
                           body=body,
                           dont_filter=True)
        if paginate:
            span_pag = response.xpath("//span[@class='negrita']/text()")[1].extract()
            current, end = pag_re.findall(span_pag)[0]
            print("current " + current)
            print("end " + end)
            if int(current) < int(end):
                # paginate
                url_request = self.principal_url + ";jsessionid=" + self.hash_session
                body = "&".join(self.formdata_pag)
                yield scrapy.Request(url_request, callback=self.parse_rows,
                                      method='POST', headers=self.new_headers,
                                      body=body,
                                      dont_filter=True)

    def get_popup(self, response):
        """
        After send popup post, we must proceed to send GET url to parse popup info
        """
        return scrapy.Request(self.url_popup, callback=self.popup_parser,
                              method='GET', headers=self.new_headers,
                              dont_filter=True)
    
    def popup_parser(self, response):
        """
        Html wich have the info
        """
        item = HojaInsumoItem()
        item['numero'] = response.xpath('//td[@id="j_id3:0:j_id13"]/text()').extract()[0]
        item['sede'] = response.xpath('//td[@id="j_id3:0:j_id15"]/text()').extract()[0]
        item['importancia'] = response.xpath('//td[@id="j_id3:0:j_id17"]/text()').extract()[0]
        item['tipo'] = response.xpath('//td[@id="j_id3:0:j_id19"]/text()').extract()[0]
        item['fecha'] = response.xpath('//td[@id="j_id21:0:j_id29"]/text()').extract()[0]
        item['ficha'] = response.xpath('//td[@id="j_id21:0:j_id31"]/text()').extract()[0]
        item['procedimiento'] = response.xpath('//td[@id="j_id21:0:j_id33"]/text()').extract()[0]
#         item['redactor_nombre']
#         item['redactor_cargo']
#         item['resumen']
#         item['sentencia']
#         res = response.xpath("//table[@class='rich-table gridcell']")
#         with open('third_req.html', 'w') as f:
#             f.write(response.body)
        return item

        
        