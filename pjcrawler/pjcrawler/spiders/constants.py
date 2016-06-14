'''
Created on Jun 10, 2016

@author: gonza
'''
import re

SESSION_RE = re.compile("JSESSIONID=.*\d+")
SESSHASH_RE = re.compile("JSESSIONID=\w*~(.+)")
POPUP_RE = re.compile("/BJNPUBLICA/hojaInsumo2.seam\?cid=\d+")
PAG_RE = re.compile(".*(\d) de (\d+)")
STANDAR_ROW = "formResultados%3AdataTable%3AX%3AlinkTituloSentencia="\
    "formResultados%3AdataTable%3AX%3AlinkTituloSentencia&"

REQUEST_HEADERS = {
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

FORMDATA = ["AJAXREQUEST=_viewRoot",
            "formBusqueda%3Aj_id18=true",
            "formBusqueda%3Aj_id20%3Aj_id23%3AfechaDesdeCalInputDate=01%2F01%2F2002",
            #"formBusqueda%3Aj_id20%3Aj_id23%3AfechaDesdeCalInputDate=27%2F05%2F2016",
             
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
 
             
            "formBusqueda%3Aj_id20%3Aj_id160%3AayudanteResumen=",
            "formBusqueda%3Aj_id20%3AdecorRedactor%3AcbxRedactorcomboboxField=AND",
            "formBusqueda%3Aj_id20%3AdecorRedactor%3AcbxRedactor=AND",
            "formBusqueda%3Aj_id20%3AdecorRedactor%3ARedactorBox=",
            "formBusqueda%3Aj_id20%3AdecorRedactor%3AsuggestRedactor_selection=",
            "formBusqueda%3Aj_id20%3AdecorNumero%3AayudanteNumero=",
            "formBusqueda%3Aj_id20%3AdecorImportancia%3AtodasLasImportancias=on",
             
            "formBusqueda%3Aj_id20%3Aj_id223%3AcantPagcomboboxField=200", # PROBAR CON NUMERO GRANDE
            "formBusqueda%3Aj_id20%3Aj_id223%3AcantPag=200", # PROBAR CON NUMERO GRANDE
             
            "formBusqueda%3Aj_id20%3Aj_id240%3Aj_id248=RELEVANCIA",
            "formBusqueda=formBusqueda=",
            "autoScroll=",          
            "formBusqueda%3Aj_id20%3ASearch=formBusqueda%3Aj_id20%3ASearch=",
            "AJAX%3AEVENTS_COUNT=1&"]

FORMDATA_POPUP = ["AJAXREQUEST=_viewRoot",
                  "formResultados=formResultados",
                  "autoScroll=",
                  "AJAX%3AEVENTS_COUNT=1"]

FORMDATA_PAG = ["AJAXREQUEST=_viewRoot",
                "formResultados=formResultados",
                "autoScroll=",
                "formResultados%3AsigLink=formResultados%3AsigLink&",
                "AJAX%3AEVENTS_COUNT=1"]
