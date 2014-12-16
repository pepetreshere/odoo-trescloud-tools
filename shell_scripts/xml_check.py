#!/usr/bin/python
#coding: utf-8

try:
    from lxml import etree
except ImportError as e:
    print """
-------------------------------------------
Falla al validar un archivo xml. Te falta instalar lmxl 2.3.2.
Prueba estos comandos en consola (requieren privilegio de administrador):
    apt-get install python-pip
    pip install lxml==2.3.2
-------------------------------------------
"""
    sys.exit(1)

try:
    import argparse
except ImportError as e:
    print """
-------------------------------------------
Falla al validar un archivo xml. Te falta instalar argparse 1.2.1.
Prueba estos comandos en consola (requieren privilegio de administrador):
    apt-get install python-pip
    pip install argparse==1.2.1
-------------------------------------------
"""
    sys.exit(1)

parser = argparse.ArgumentParser(description=u"Toma un esquema xml (.xsd) e intenta validar muchos archivos", epilog="El primer argumento pasado es el camino absoluto a un archivo .xsd, mientras que los siguientes argumentos son caminos absolutos, cada uno, a archivos .xml a validar con ese .xsd")
parser.add_argument('xsd', metavar='schema', help=u"Archivo para usar como esquema de validación")
parser.add_argument('xml', metavar='xmls', nargs='+', help=u"Uno o más archivos xml a ser validados por el esquema de validación")

args = parser.parse_args()

import sys

print """
----------
----------------------------
--------------------------------------------------
Utilitario de TRESCLOUD para validar archivos XML.
--------------------------------------------------
                      ----------------------------
                                        ----------
"""

print """
----> Cargando hoja de esquema:
----> %s
""" % args.xsd

try:
    parser = etree.XMLParser(schema = etree.XMLSchema(etree.parse(args.xsd)))
except etree.XMLSyntaxError as e:
    print """
----> Archivo xsd inválido:
----> %s
----> Error: %s
""" % (args.xsd, e)
    sys.exit(1)
except IOError as e:
    print """
----> Archivo inaccesible:
----> %s
----> Error: %s
""" % (args.xsd, e)
    sys.exit(1)
except Exception as e:
    print """
----> Error procesando archivo:
----> %s
----> Error: %s
""" % (args.xsd, e)
    sys.exit(1)

for f in args.xml:
    print """
---> Intentando leer archivo:
---> %s
""" % f
    try:
        root = etree.parse(f, parser)
        print """
----> Archivo válido:
----> %s
""" % f
    except etree.XMLSyntaxError as e:
        print """
----> Archivo xml inválido:
----> %s
----> Error: %s
""" % (f, e)
    except IOError as e:
        print """
----> Archivo inaccesible:
----> %s
----> Error: %s
""" % (f, e)
    except Exception as e:
        print """
----> Error procesando archivo:
----> %s
----> Error: %s
""" % (f, e)
