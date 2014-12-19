#!/usr/bin/python
# coding: utf-8


from xml_check import validate_doc, XSD_SRI_110_FACTURA, XSD_SRI_110_NOTACRED, XMLDocumentException, XMLValidationException, XMLFormatException


factura_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<factura id="comprobante" version="1.1.0">
    <infoTributaria>
        <ambiente>1</ambiente>
        <tipoEmision>1</tipoEmision>
        <razonSocial>XYZ</razonSocial>
        <nombreComercial>XYZ</nombreComercial>
        <ruc>0000000000001</ruc>
        <claveAcceso>2103201301000000000000110015010000000101234567811</claveAcceso>
        <codDoc>01</codDoc>
        <estab>001</estab>
        <ptoEmi>501</ptoEmi>
        <secuencial>000000010</secuencial>
        <dirMatriz>AMAZONAS</dirMatriz>
    </infoTributaria>
    <infoFactura>
        <fechaEmision>21/03/2013</fechaEmision>
        <dirEstablecimiento>AMAZONAS</dirEstablecimiento>
        <contribuyenteEspecial>12345</contribuyenteEspecial>
        <obligadoContabilidad>SI</obligadoContabilidad>
        <tipoIdentificacionComprador>04</tipoIdentificacionComprador>
        <razonSocialComprador>SRI PRUEBAS</razonSocialComprador>
        <identificacionComprador>1760013210001</identificacionComprador>
        <totalSinImpuestos>0.00</totalSinImpuestos>
        <totalDescuento>0.00</totalDescuento>
        <totalConImpuestos>
            <totalImpuesto>
                <codigo>2</codigo>
                <codigoPorcentaje>6</codigoPorcentaje>
				<descuentoAdicional>0</descuentoAdicional>
                <baseImponible>0.00</baseImponible>
                <valor>0.00</valor>
            </totalImpuesto>
            <totalImpuesto>
                <codigo>3</codigo>
                <codigoPorcentaje>3011</codigoPorcentaje>
                <baseImponible>0.00</baseImponible>
                <valor>0.00</valor>
            </totalImpuesto>
        </totalConImpuestos>
        <propina>0.00</propina>
        <importeTotal>0.00</importeTotal>
        <moneda>DOLAR</moneda>
    </infoFactura>
    <detalles>
        <detalle>
            <codigoPrincipal>011</codigoPrincipal>
            <descripcion>PRUEBA</descripcion>
            <cantidad>0.000000</cantidad>
            <precioUnitario>0.000000</precioUnitario>
            <descuento>0</descuento>
            <precioTotalSinImpuesto>0.00</precioTotalSinImpuesto>
            <impuestos>
                <impuesto>
                    <codigo>2</codigo>
                    <codigoPorcentaje>6</codigoPorcentaje>
                    <tarifa>0.00</tarifa>
                    <baseImponible>0.00</baseImponible>
                    <valor>0.00</valor>
                </impuesto>
                <impuesto>
                    <codigo>3</codigo>
                    <codigoPorcentaje>3011</codigoPorcentaje>
                    <tarifa>0.00</tarifa>
                    <baseImponible>0.00</baseImponible>
                    <valor>0.00</valor>
                </impuesto>
            </impuestos>
        </detalle>
    </detalles>
	<retenciones>
        <retencion>
	    <codigo>4</codigo>
	    <codigoPorcentaje>327</codigoPorcentaje>
	    <tarifa>0.00</tarifa>	    
	    <valor>0.00</valor>
        </retencion>
        <retencion>
	    <codigo>4</codigo>
	    <codigoPorcentaje>328</codigoPorcentaje>
	    <tarifa>0.00</tarifa>	    
	    <valor>0.00</valor>
        </retencion>
	<retencion>
	    <codigo>4</codigo>
	    <codigoPorcentaje>3</codigoPorcentaje>
	    <tarifa>1</tarifa>	    
	    <valor>0.00</valor>
        </retencion>
    </retenciones>
    <infoAdicional>
        <campoAdicional nombre="Dirección">xyz</campoAdicional>
        <campoAdicional nombre="Email">sri@gob.ec</campoAdicional>
    </infoAdicional>
</factura>"""


notacred_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<notaCredito id="comprobante" version="1.1.0">
    <infoTributaria>
        <ambiente>1</ambiente>
        <tipoEmision>1</tipoEmision>
        <razonSocial>XYZ</razonSocial>
        <nombreComercial>XYZ</nombreComercial>
        <ruc>0000000000001</ruc>
        <claveAcceso>2103201304000000000000110015010000000471234567812</claveAcceso>
        <codDoc>04</codDoc>
        <estab>001</estab>
        <ptoEmi>501</ptoEmi>
        <secuencial>000000047</secuencial>
        <dirMatriz>AMAZONAS</dirMatriz>
    </infoTributaria>
    <infoNotaCredito>
        <fechaEmision>21/03/2013</fechaEmision>
        <dirEstablecimiento>AMAZONAS</dirEstablecimiento>
        <tipoIdentificacionComprador>04</tipoIdentificacionComprador>
        <razonSocialComprador>SRI PRUEBAS</razonSocialComprador>
        <identificacionComprador>1760013210001</identificacionComprador>
        <contribuyenteEspecial>12345</contribuyenteEspecial>
        <obligadoContabilidad>SI</obligadoContabilidad>
        <codDocModificado>01</codDocModificado>
        <numDocModificado>001-001-000000000</numDocModificado>
        <fechaEmisionDocSustento>20/03/2013</fechaEmisionDocSustento>
        <totalSinImpuestos>0.00</totalSinImpuestos>
        <valorModificacion>0.00</valorModificacion>
        <moneda>DOLAR</moneda>
        <totalConImpuestos>
            <totalImpuesto>
                <codigo>2</codigo>
                <codigoPorcentaje>6</codigoPorcentaje>
                <baseImponible>0.00</baseImponible>
                <valor>0.00</valor>
            </totalImpuesto>
            <totalImpuesto>
                <codigo>3</codigo>
                <codigoPorcentaje>3011</codigoPorcentaje>
                <baseImponible>0.00</baseImponible>
                <valor>0</valor>
            </totalImpuesto>
        </totalConImpuestos>
        <motivo>abcd</motivo>
    </infoNotaCredito>
    <detalles>
        <detalle>
            <codigoInterno>011</codigoInterno>
            <descripcion>PRUEBA</descripcion>
            <cantidad>0.000000</cantidad>
            <precioUnitario>0.000000</precioUnitario>
            <descuento>0</descuento>
            <precioTotalSinImpuesto>0.00</precioTotalSinImpuesto>
            <impuestos>
                <impuesto>
                    <codigo>2</codigo>
                    <codigoPorcentaje>6</codigoPorcentaje>
                    <tarifa>0.00</tarifa>
                    <baseImponible>0.00</baseImponible>
                    <valor>0.00</valor>
                </impuesto>
                <impuesto>
                    <codigo>3</codigo>
                    <codigoPorcentaje>3011</codigoPorcentaje>
                    <tarifa>0.00</tarifa>
                    <baseImponible>0.00</baseImponible>
                    <valor>0</valor>
                </impuesto>
            </impuestos>
        </detalle>
    </detalles>
    <infoAdicional>
        <campoAdicional nombre="Dirección">xyz</campoAdicional>
        <campoAdicional nombre="Email">sri@gob.ec</campoAdicional>
    </infoAdicional>
</notaCredito>"""

try:
    validate_doc(factura_xml, XSD_SRI_110_FACTURA)
    validate_doc(notacred_xml, XSD_SRI_110_NOTACRED)
    print u"documento validado exitosamente"
except XMLFormatException as e:
    print u"hubo error en %s: %s" % ({1:"el archivo xml", 2:"el archivo xsd"}[e.args[1]], e.args[0])
except XMLValidationException as e:
    print u"hubo un error al intentar validar el xml contra el xsd. log de error: %r" % e.args[1]
