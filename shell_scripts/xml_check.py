#coding: utf-8
from lxml import etree


class XMLDocumentException(Exception):
    u"""
    Un error relacionado a la validacion de
    un documento xml.
    """
    pass


class XMLFormatException(XMLDocumentException):
    u"""
    Esta excepcion se gatilla cuando la validacion
    de un string xml da mala (sea para un xml o para
    un archivo xsd). El mensaje incluido por esta
    excepcion es directamente el mensaje que proporciona
    la libreria xml (por lo que el mensaje sale en ingles).
    Adicionalmente, se incluye un segundo argumento que es
    un distintivo de donde ocurrio esta excepcion (IN_XML
    para cuando ocurra dentro del archivo XML, o IN_XSD para
    cuando ocurra en el archivo xsd). Capturada esta excepcion,
    dicho valor lo podemos obtener como:
         try:
             validate_xml_document(..., ..., ...)
         except XMLFormatException as e:
             mensaje = e.args[0]
             donde = e.args[1]
    """
    IN_XML = 1
    IN_XSD = 2


class XMLValidationException(XMLDocumentException):
    u"""
    Esta excepcion se gatilla cuando la validacion
    entre un xml y su xsd da mala. El mensaje incluido
    por esta excepcion es directamente el mensaje que
    proporciona la libreria lxml (por lo que el mensaje
    sale en ingles). Esta excepción muestra un mensaje
    y un log de validación, por lo que al encontrarla
    deberíamos obtener esos valores. El log de validación
    es una estructura propia de la librería lxml, por lo
    que los mensajes de validación estarán en inglés.
    Deberíamos capturar la excepción de esta manera:
         try:
             validate_xml_document(..., ..., ...)
         except XMLFormatException as e:
             mensaje = e.args[0]
             error_log = e.args[1]

    La estructura de error_log está documentada en:
        http://lxml.de/parsing.html
    """
    pass


#esta excepcion en cuestion no la vamos a usar
#hasta que le pongamos realmente un "gancho" que
#nos oficie de validador semantico
class SemanticValidationException(XMLDocumentException):
    u"""
    Deberiamos hacer uso de esta excepcion dentro de
    nuestra funcion de validacion semantica. Esta
    excepcion deberia lanzarse asi:
        raise SemanticValidationException("El codigo no corresponde")
    """
    pass


XSD_SRI_110_FACTURA = """<?xml version="1.0" encoding="UTF-8"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
	xmlns:ds="http://www.w3.org/2000/09/xmldsig#" elementFormDefault="qualified">
	<xsd:import namespace="http://www.w3.org/2000/09/xmldsig#"
		schemaLocation="http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd#"/>
	<xsd:simpleType name="ambiente">
		<xsd:annotation>
			<xsd:documentation>Desarrollo o produccion depende de en cual ambiente se genere el comprobante.</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[1-2]{1}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="razonSocial">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="dirMatriz">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="nombreComercial">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:complexType name="infoTributaria">
		<xsd:annotation>
			<xsd:documentation>Contiene la informacion tributaria generica</xsd:documentation>
		</xsd:annotation>
		<xsd:sequence>
			<xsd:element name="ambiente" type="ambiente"/>
			<xsd:element name="tipoEmision" type="tipoEmision"/>
			<xsd:element name="razonSocial" type="razonSocial"/>
			<xsd:element name="nombreComercial" minOccurs="0" type="nombreComercial"/>
			<xsd:element name="ruc" type="numeroRuc"/>
			<xsd:element name="claveAcceso" type="claveAcceso"/>
			<xsd:element name="codDoc" type="codDoc"/>
			<xsd:element name="estab" type="establecimiento"/>
			<xsd:element name="ptoEmi" type="puntoEmision"/>
			<xsd:element name="secuencial" type="secuencial"/>
			<xsd:element name="dirMatriz" type="dirMatriz"/>
		</xsd:sequence>
	</xsd:complexType>
	<xsd:simpleType name="numeroRuc">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero de RUC del Contribuyente</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{10}001"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="idCliente">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero de RUC Cedula o Pasaporte del Comprador</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="13"/>
			<xsd:pattern value="[0-9a-zA-Z]{0,13}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="numeroRucCedula">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero de RUC o cedula del Comprador</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="10"/>
			<xsd:maxLength value="13"/>
			<xsd:pattern value="[0-9]{10}"/>
			<xsd:pattern value="[0-9]{10}001"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaType">
		<xsd:annotation>
			<xsd:documentation>Se detalla la fecha de uso del documento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaAutorizacion">
		<xsd:annotation>
			<xsd:documentation>Se detalla la fecha de la autorizacion</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="establecimiento">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero del establecimiento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="puntoEmision">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero del punto de emision</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="secuencial">
		<xsd:annotation>
			<xsd:documentation>Se detalla el secuencial del documento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{9}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="documento">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero del documento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}-[0-9]{3}-[0-9]{1,9}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codTipoDoc">
		<xsd:annotation>
			<xsd:documentation>Se detalla el codigo del tipo de documento autorizado</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]+"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codTipoDocModificado">
		<xsd:annotation>
			<xsd:documentation>Se detalla el codigo del tipo de documento autorizado</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:integer">
			<xsd:minInclusive value="1"/>
			<xsd:maxInclusive value="8"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="claveAcceso">
		<xsd:annotation>
			<xsd:documentation>Se guarda la informacion para la clave de acceso</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{49}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="autorizacion">
		<xsd:annotation>
			<xsd:documentation>Corresponde al numero de autorizacion emitido por el sistema de Autorizacion de Comprobantes de Venta y Retencion</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:maxLength value="10"/>
			<xsd:minLength value="3"/>
			<xsd:pattern value="[0-9]{3,10}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaEmision">
		<xsd:restriction base="xsd:string">
			<xsd:pattern
				value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="dirEstablecimiento">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tipoEmision">
		<xsd:annotation>
			<xsd:documentation>Tipo de emision en el cual se genero el comprobante</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[12]{1}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="contribuyenteEspecial">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="3"/>
			<xsd:maxLength value="13"/>
			<xsd:pattern value="([A-Za-z0-9])*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="obligadoContabilidad">
		<xsd:restriction base="xsd:string">
			<xsd:enumeration value="SI"/>
			<xsd:enumeration value="NO"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tipoIdentificacionComprador">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0][4-9]"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="guiaRemision">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}-[0-9]{3}-[0-9]{9}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="razonSocialComprador">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="identificacionComprador">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="20"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="totalSinImpuestos">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigo">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]+"/>
			<xsd:minLength value="1"/>
			<xsd:maxLength value="1"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codDoc">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="totalDescuentos">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="descuentoAdicional">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
		</xsd:restriction>
	</xsd:simpleType>		
	<xsd:simpleType name="codigoPorcentaje">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]+"/>
			<xsd:minLength value="1"/>
			<xsd:maxLength value="4"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="baseImponible">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tarifa">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="4"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="valor">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="valorDevolucionIva">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="propina">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="importeTotal">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="moneda">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="15"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoPrincipal">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="25"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoAuxiliar">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="25"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="descripcion">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="cantidad">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="18"/>
			<xsd:fractionDigits value="6"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="precioUnitario">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="18"/>
			<xsd:fractionDigits value="6"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="descuento">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="precioTotalSinImpuesto">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="nombre">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="campoAdicional">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoRetencion">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[4]{1}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoPorcentajeRetencion">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{1,3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tarifaRetencion">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="5"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="valorRetencion">
		<xsd:restriction base="xsd:decimal">
			<xsd:fractionDigits value="2"/>
			<xsd:totalDigits value="14"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="comercioExterior">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="EXPORTADOR"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="incoTermFactura">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="10"/>
			<xsd:pattern value="([A-Z])*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="lugarIncoTerm">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="paisOrigen">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="paisDestino">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="puertoEmbarque">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="puertoDestino">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="paisAdquisicion">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="direccionComprador">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="incoTermTotalSinImpuestos">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="10"/>
			<xsd:pattern value="([A-Z])*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fleteInternacional">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="seguroInternacional">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="gastosAduaneros">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="gastosTransporteOtros">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="formaPago">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0][1-9]"/>
			<xsd:pattern value="[1][0-5]"/>
		</xsd:restriction>
	</xsd:simpleType>	
	<xsd:simpleType name="total">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="plazo">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>	
	<xsd:simpleType name="unidadTiempo">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="10"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="unidadMedida">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="50"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:complexType name="pagos">	
		<xsd:sequence>
			<xsd:element name="pago" minOccurs="1" maxOccurs="unbounded">
				<xsd:complexType>
					<xsd:sequence>
						<xsd:element name="formaPago" minOccurs="1" type="formaPago"/>
						<xsd:element name="total" minOccurs="1" type="total"/>
						<xsd:element name="plazo" minOccurs="0" type="plazo"/>
						<xsd:element name="unidadTiempo" minOccurs="0" type="unidadTiempo"/>
					</xsd:sequence>
				</xsd:complexType>
			</xsd:element>						
		</xsd:sequence>
	</xsd:complexType>
	<xsd:complexType name="impuesto">
		<xsd:annotation>
			<xsd:documentation>Contiene la informacion de los impuestos</xsd:documentation>
		</xsd:annotation>
		<xsd:sequence>
			<xsd:element name="codigo" type="codigo"/>
			<xsd:element name="codigoPorcentaje" type="codigoPorcentaje"/>
			<xsd:element name="tarifa" type="tarifa" minOccurs="1"/>
			<xsd:element name="baseImponible" type="baseImponible" minOccurs="1"/>
			<xsd:element name="valor" type="valor"/>
		</xsd:sequence>
	</xsd:complexType>
	<xsd:simpleType name="codigoDocumentoReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="41"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="totalComprobantesReembolso">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="totalBaseImponibleReembolso">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="totalImpuestoReembolso">	
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="valorRetIva">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>	
	<xsd:simpleType name="valorRetRenta">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tipoIdentificacionProveedorReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0][4-9]"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="identificacionProveedorReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="20"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codPaisPagoProveedorReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tipoProveedorReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0][12]"/>
		</xsd:restriction>
	</xsd:simpleType>	
	<xsd:simpleType name="codDocReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:enumeration value="01"/>
			<xsd:enumeration value="04"/>
			<xsd:enumeration value="05"/>
			<xsd:enumeration value="06"/>
			<xsd:enumeration value="07"/>
			<xsd:enumeration value="41"/>
			<xsd:enumeration value="19"/>
		</xsd:restriction>
	</xsd:simpleType>	
	<xsd:simpleType name="estabDocReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="ptoEmiDocReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="secuencialDocReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{9}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaEmisionDocReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:pattern
				value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="numeroautorizacionDocReemb">
		<xsd:restriction base="xsd:string">
			<xsd:maxLength value="37"/>
			<xsd:minLength value="10"/>
			<xsd:pattern value="[0-9]{10,37}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoReembolso">	
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[235]"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoPorcentajeReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{1,4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tarifaReembolso">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{1,4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="baseImponibleReembolso">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="impuestoReembolso">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:complexType name="detalleImpuestos">	
		<xsd:sequence>
			<xsd:element name="detalleImpuesto" minOccurs="1" maxOccurs="unbounded">
				<xsd:complexType>
					<xsd:sequence>
						<xsd:element name="codigo" minOccurs="1" type="codigoReembolso"/>
						<xsd:element name="codigoPorcentaje" minOccurs="1" type="codigoPorcentajeReembolso"/>
						<xsd:element name="tarifa" minOccurs="1" type="tarifaReembolso"/>
						<xsd:element name="baseImponibleReembolso" minOccurs="1" type="baseImponibleReembolso"/>
						<xsd:element name="impuestoReembolso" minOccurs="1" type="impuestoReembolso"/>							
					</xsd:sequence>
				</xsd:complexType>
			</xsd:element>						
		</xsd:sequence>
	</xsd:complexType>
	<xsd:complexType name="reembolsos">	
		<xsd:sequence>
			<xsd:element name="reembolsoDetalle" minOccurs="1" maxOccurs="unbounded">
				<xsd:complexType>
					<xsd:sequence>
						<xsd:element name="tipoIdentificacionProveedorReembolso" minOccurs="1" type="tipoIdentificacionProveedorReembolso"/>
						<xsd:element name="identificacionProveedorReembolso" minOccurs="1" type="identificacionProveedorReembolso"/>
						<xsd:element name="codPaisPagoProveedorReembolso" minOccurs="0" type="codPaisPagoProveedorReembolso"/>
						<xsd:element name="tipoProveedorReembolso" minOccurs="1" type="tipoProveedorReembolso"/>						
						<xsd:element name="codDocReembolso" minOccurs="1" type="codDocReembolso"/>
						<xsd:element name="estabDocReembolso" minOccurs="1" type="estabDocReembolso"/>
						<xsd:element name="ptoEmiDocReembolso" minOccurs="1" type="ptoEmiDocReembolso"/>
						<xsd:element name="secuencialDocReembolso" minOccurs="1" type="secuencialDocReembolso"/>
						<xsd:element name="fechaEmisionDocReembolso" minOccurs="1" type="fechaEmisionDocReembolso"/>	
						<xsd:element name="numeroautorizacionDocReemb" minOccurs="1" type="numeroautorizacionDocReemb"/>
						<xsd:element name="detalleImpuestos" minOccurs="1" type="detalleImpuestos"/>
					</xsd:sequence>
				</xsd:complexType>
			</xsd:element>						
		</xsd:sequence>
	</xsd:complexType>
	<xsd:element name="factura">
		<xsd:complexType>
			<xsd:sequence>
				<xsd:element name="infoTributaria" type="infoTributaria"/>
				<xsd:element name="infoFactura">
					<xsd:complexType>
						<xsd:sequence>
							<xsd:element name="fechaEmision" type="fechaEmision"> </xsd:element>
							<xsd:element name="dirEstablecimiento" type="dirEstablecimiento" minOccurs="0"/>
							<xsd:element name="contribuyenteEspecial" type="contribuyenteEspecial" minOccurs="0"/>
							<xsd:element name="obligadoContabilidad" minOccurs="0"	type="obligadoContabilidad"/>
							<xsd:element name="comercioExterior" minOccurs="0"	type="comercioExterior"/>
							<xsd:element name="incoTermFactura" minOccurs="0"	type="incoTermFactura"/>
							<xsd:element name="lugarIncoTerm" minOccurs="0"	type="lugarIncoTerm"/>
							<xsd:element name="paisOrigen" minOccurs="0"	type="paisOrigen"/>
							<xsd:element name="puertoEmbarque" minOccurs="0"	type="puertoEmbarque"/>
							<xsd:element name="puertoDestino" minOccurs="0"	type="puertoDestino"/>
							<xsd:element name="paisDestino" minOccurs="0"	type="paisDestino"/>
							<xsd:element name="paisAdquisicion" minOccurs="0"	type="paisAdquisicion"/>
							<xsd:element name="tipoIdentificacionComprador"	type="tipoIdentificacionComprador"/>
							<xsd:element name="guiaRemision" minOccurs="0" type="guiaRemision"/>
							<xsd:element name="razonSocialComprador" type="razonSocialComprador"/>
							<xsd:element name="identificacionComprador"	type="identificacionComprador"/>
							<xsd:element name="direccionComprador"  minOccurs="0" type="direccionComprador"/>
							<xsd:element name="totalSinImpuestos" type="totalSinImpuestos"/>
							<xsd:element name="incoTermTotalSinImpuestos"  minOccurs="0" type="incoTermTotalSinImpuestos"/>
							<xsd:element name="totalDescuento" type="totalDescuentos"/>
							<xsd:element name="codDocReembolso" minOccurs="0" type="codigoDocumentoReembolso"/>							
							<xsd:element name="totalComprobantesReembolso" minOccurs="0" type="totalComprobantesReembolso"/>		
							<xsd:element name="totalBaseImponibleReembolso" minOccurs="0" type="totalBaseImponibleReembolso"/>	
							<xsd:element name="totalImpuestoReembolso" minOccurs="0" type="totalImpuestoReembolso"/>	
							<xsd:element name="totalConImpuestos">
								<xsd:complexType>
									<xsd:sequence>
										<xsd:element name="totalImpuesto" maxOccurs="unbounded">
											<xsd:complexType>
												<xsd:sequence>
												<xsd:element name="codigo" type="codigo"/>
												<xsd:element name="codigoPorcentaje" type="codigoPorcentaje"/>
												<xsd:element name="descuentoAdicional" minOccurs="0" type="descuentoAdicional"/>
												<xsd:element name="baseImponible" type="baseImponible"/>												
												<xsd:element name="tarifa" type="tarifa" minOccurs="0"/>
												<xsd:element name="valor" minOccurs="1"	type="valor"/>
												<xsd:element name="valorDevolucionIva" type="valorDevolucionIva" minOccurs="0"/>
												</xsd:sequence>
											</xsd:complexType>
										</xsd:element>
									</xsd:sequence>
								</xsd:complexType>
							</xsd:element>
							<xsd:element name="propina" type="propina" minOccurs="1"/>
							<xsd:element name="fleteInternacional"  minOccurs="0" type="fleteInternacional"/>
							<xsd:element name="seguroInternacional"  minOccurs="0" type="seguroInternacional"/>
							<xsd:element name="gastosAduaneros"  minOccurs="0" type="gastosAduaneros"/>
							<xsd:element name="gastosTransporteOtros"  minOccurs="0" type="gastosTransporteOtros"/>
							<xsd:element name="importeTotal" type="importeTotal"/>
							<xsd:element name="moneda" minOccurs="0" type="moneda"/>
							<xsd:element name="pagos" minOccurs="0" type="pagos"/>
							<xsd:element name="valorRetIva" minOccurs="0" type="valorRetIva"/>
							<xsd:element name="valorRetRenta" minOccurs="0" type="valorRetRenta"/>
						</xsd:sequence>
					</xsd:complexType>
				</xsd:element>
				<xsd:element name="detalles">
					<xsd:complexType>
						<xsd:sequence>
							<xsd:element name="detalle" minOccurs="1" maxOccurs="unbounded">
								<xsd:complexType>
									<xsd:sequence>
										<xsd:element name="codigoPrincipal" minOccurs="0" type="codigoPrincipal"/>
										<xsd:element name="codigoAuxiliar" minOccurs="0" type="codigoAuxiliar"/>
										<xsd:element name="descripcion" type="descripcion"/>
										<xsd:element name="unidadMedida" minOccurs="0" type="unidadMedida"/>
										<xsd:element name="cantidad" type="cantidad"/>
										<xsd:element name="precioUnitario" type="precioUnitario"/>
										<xsd:element name="descuento" minOccurs="1" type="descuento"/>
										<xsd:element name="precioTotalSinImpuesto" type="precioTotalSinImpuesto"/>
										<xsd:element name="detallesAdicionales" minOccurs="0">
											<xsd:complexType>
												<xsd:sequence>
													<xsd:element name="detAdicional" maxOccurs="3">
														<xsd:complexType>
															<xsd:attribute name="nombre">
																<xsd:simpleType>
																	<xsd:restriction base="xsd:string">
																		<xsd:pattern value="[^\\n]*"/>
																		<xsd:minLength value="1"/>
																		<xsd:maxLength value="300"/>
																	</xsd:restriction>
																</xsd:simpleType>
															</xsd:attribute>
															<xsd:attribute name="valor">
																<xsd:simpleType>
																	<xsd:restriction base="xsd:string">
																		<xsd:pattern value="[^\\n]*"/>
																		<xsd:minLength value="1"/>
																		<xsd:maxLength value="300"/>
																	</xsd:restriction>
																</xsd:simpleType>
															</xsd:attribute>
														</xsd:complexType>
													</xsd:element>
												</xsd:sequence>
											</xsd:complexType>
										</xsd:element>
										<xsd:element name="impuestos">
											<xsd:complexType>
												<xsd:sequence>
													<xsd:element name="impuesto" type="impuesto" maxOccurs="unbounded"/>
												</xsd:sequence>
											</xsd:complexType>
										</xsd:element>
									</xsd:sequence>
								</xsd:complexType>
							</xsd:element>
						</xsd:sequence>
					</xsd:complexType>
				</xsd:element>
				<xsd:element name="reembolsos" minOccurs="0" type="reembolsos"/>
				<xsd:element minOccurs="0" name="retenciones">
					<xsd:complexType>
						<xsd:sequence>
							<xsd:element maxOccurs="unbounded" name="retencion">
								<xsd:complexType>
									<xsd:sequence>
										<xsd:element name="codigo" type="codigoRetencion"/>
										<xsd:element name="codigoPorcentaje" type="codigoPorcentajeRetencion"/>
										<xsd:element name="tarifa" type="tarifaRetencion"/>
										<xsd:element name="valor" type="valorRetencion"/>
									</xsd:sequence>
								</xsd:complexType>
							</xsd:element>
						</xsd:sequence>
					</xsd:complexType>
				</xsd:element>
				<xsd:element name="infoAdicional" minOccurs="0">
					<xsd:complexType>
						<xsd:sequence>
							<xsd:element maxOccurs="15" name="campoAdicional">
								<xsd:complexType>
									<xsd:simpleContent>
										<xsd:extension base="campoAdicional">
											<xsd:attribute name="nombre" type="nombre"/>
										</xsd:extension>
									</xsd:simpleContent>
								</xsd:complexType>
							</xsd:element>
						</xsd:sequence>
					</xsd:complexType>
				</xsd:element>
				<xsd:element ref="ds:Signature" minOccurs="0">
					<xsd:annotation>
						<xsd:documentation xml:lang="en"> Set of data associated with the invoice which guarantee the authorship and integrity of the message. It is defined as optional to ease the validation and transmission of the file. However, this block of electronic signature must be completed in order for an electronic invoice to be considered legally valid before third parties.</xsd:documentation>
						<xsd:documentation xml:lang="es"> Conjunto de datos asociados a la factura que garantizarán la autoría y la integridad del mensaje. Se define como opcional para facilitar la verificación y el tránsito del fichero. No obstante, debe cumplimentarse este bloque de firma electrónica para que se considere una factura electrónica válida legalmente frente a terceros.</xsd:documentation>
					</xsd:annotation>
				</xsd:element>
			</xsd:sequence>
			<xsd:attribute name="id">
				<xsd:simpleType>
					<xsd:restriction base="xsd:string">
						<xsd:enumeration value="comprobante"/>
					</xsd:restriction>
				</xsd:simpleType>
			</xsd:attribute>
			<xsd:attribute name="version"/>
		</xsd:complexType>
	</xsd:element>
</xsd:schema>"""


XSD_SRI_110_NOTACRED = """
<?xml version="1.1" encoding="UTF-8"?>
<!-- edited with XMLSPY v5 rel. 3 U (http://www.xmlspy.com) by ALEJANDRO SUBIA (SERVICIO DE RENTAS INTERNAS) -->
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
	xmlns:ds="http://www.w3.org/2000/09/xmldsig#" elementFormDefault="qualified">
	<xsd:import namespace="http://www.w3.org/2000/09/xmldsig#"
		schemaLocation="http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd#"/>
	<xsd:simpleType name="numeroRuc">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero de RUC del Contribuyente</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{10}001"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="idCliente">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero de RUC Cedula o Pasaporte del Comprador</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="13"/>
			<xsd:pattern value="[0-9a-zA-Z]{0,13}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="numeroRucCedula">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero de RUC o cedula del Comprador</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="10"/>
			<xsd:maxLength value="13"/>
			<xsd:pattern value="[0-9]{10}"/>
			<xsd:pattern value="[0-9]{10}001"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaType">
		<xsd:annotation>
			<xsd:documentation>Se detalla la fecha de uso del documento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaAutorizacion">
		<xsd:annotation>
			<xsd:documentation>Se detalla la fecha de la autorizacion</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="establecimiento">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero del establecimiento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="puntoEmision">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero del punto de emision</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="secuencial">
		<xsd:annotation>
			<xsd:documentation>Se detalla el secuencial del documento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{9}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="documento">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero del documento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}-[0-9]{3}-[0-9]{1,9}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codTipoDoc">
		<xsd:annotation>
			<xsd:documentation>Se detalla el codigo del tipo de documento autorizado</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:integer">
			<xsd:minInclusive value="4"/>
			<xsd:maxInclusive value="4"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codTipoDocModificado">
		<xsd:annotation>
			<xsd:documentation>Se detalla el codigo del tipo de documento autorizado</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:integer">
			<xsd:minInclusive value="1"/>
			<xsd:maxInclusive value="8"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="claveAcceso">
		<xsd:annotation>
			<xsd:documentation>Se guarda la informacion para la clave de acceso</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{49}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="autorizacion">
		<xsd:annotation>
			<xsd:documentation>Corresponde al numero de autorizacion emitido por el sistema de Autorizacion de Comprobantes de Venta y Retencion
                    </xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:maxLength value="10"/>
			<xsd:minLength value="3"/>
			<xsd:pattern value="[0-9]{3,10}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="ambiente">
		<xsd:annotation>
			<xsd:documentation>Desarrollo o produccion depende de en cual ambiente se genere el comprobante.</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[1-2]{1}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tipoEmision">
		<xsd:annotation>
			<xsd:documentation>Tipo de emision en el cual se genero el comprobante</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[12]{1}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="razonSocial">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="nombreComercial">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="rise">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="40"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codDocModificado">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="numDocModificado">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}-[0-9]{3}-[0-9]{9}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaEmisionDocSustento">
		<xsd:restriction base="xsd:string">
			<xsd:pattern
				value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="valorModificacion">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoInterno">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="25"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoAdicional">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="25"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="motivo">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:complexType name="detalle">
		<xsd:annotation>
			<xsd:documentation>Detalle de una nota de credito.</xsd:documentation>
		</xsd:annotation>
		<xsd:sequence>
			<xsd:element name="motivoModificacion" type="xsd:string"/>
		</xsd:sequence>
	</xsd:complexType>
	<xsd:complexType name="impuesto">
		<xsd:annotation>
			<xsd:documentation>Contiene la información de los impuestos</xsd:documentation>
		</xsd:annotation>
		<xsd:sequence>
			<xsd:element name="codigo" type="codigo"/>
			<xsd:element name="codigoPorcentaje" type="codigoPorcentaje"/>
			<xsd:element name="tarifa" minOccurs="0" type="tarifa"/>
			<xsd:element name="baseImponible" minOccurs="1" type="baseImponible"/>
			<xsd:element name="valor" type="valor"/>
		</xsd:sequence>
	</xsd:complexType>
	<xsd:complexType name="infoTributaria">
		<xsd:annotation>
			<xsd:documentation>Contiene la informacion tributaria generica</xsd:documentation>
		</xsd:annotation>
		<xsd:sequence>
			<xsd:element name="ambiente" type="ambiente"/>
			<xsd:element name="tipoEmision" type="tipoEmision"/>
			<xsd:element name="razonSocial" type="razonSocial"/>
			<xsd:element name="nombreComercial" minOccurs="0" type="nombreComercial"/>
			<xsd:element name="ruc" type="numeroRuc"/>
			<xsd:element name="claveAcceso" type="claveAcceso"/>
			<xsd:element name="codDoc" type="codDoc"/>
			<xsd:element name="estab" type="establecimiento"/>
			<xsd:element name="ptoEmi" type="puntoEmision"/>
			<xsd:element name="secuencial" type="secuencial"/>
			<xsd:element name="dirMatriz" type="dirMatriz"/>
		</xsd:sequence>
	</xsd:complexType>
	<xsd:element name="notaCredito">
		<xsd:annotation>
			<xsd:documentation>Elemento que describe una nota de debito o credito</xsd:documentation>
		</xsd:annotation>
		<xsd:complexType>
			<xsd:sequence>
				<xsd:element name="infoTributaria" type="infoTributaria"/>
				<xsd:element name="infoNotaCredito">
					<xsd:complexType>
						<xsd:sequence>
							<xsd:element name="fechaEmision" type="fechaEmision"/>
							<xsd:element name="dirEstablecimiento" minOccurs="0" type="dirEstablecimiento"/>
							<xsd:element name="tipoIdentificacionComprador"	type="tipoIdentificacionComprador"/>
							<xsd:element name="razonSocialComprador" type="razonSocialComprador"/>
							<xsd:element name="identificacionComprador" minOccurs="1" type="identificacionComprador"/>
							<xsd:element name="contribuyenteEspecial" minOccurs="0"	type="contribuyenteEspecial"/>
							<xsd:element name="obligadoContabilidad" minOccurs="0"	type="obligadoContabilidad"/> 
							<xsd:element name="rise" minOccurs="0" type="rise"/>
							<xsd:element name="codDocModificado" type="codDocModificado"/>
							<xsd:element name="numDocModificado" type="numDocModificado"/>
							<xsd:element name="fechaEmisionDocSustento"	type="fechaEmisionDocSustento" minOccurs="1"/>
							<xsd:element name="totalSinImpuestos" type="totalSinImpuestos"/>
							<xsd:element name="valorModificacion" minOccurs="1"	type="valorModificacion"/> 
							<xsd:element name="moneda" minOccurs="0" type="moneda"/>
							<xsd:element ref="totalConImpuestos"/>
							<xsd:element name="motivo" type="motivo"/>
						</xsd:sequence>
					</xsd:complexType>
				</xsd:element>
				<xsd:element name="detalles">
					<xsd:complexType>
						<xsd:sequence>
							<xsd:element name="detalle" maxOccurs="unbounded" minOccurs="1">
								<xsd:complexType>
									<xsd:sequence>
										<xsd:element name="codigoInterno" minOccurs="0" type="codigoInterno"/>
										<xsd:element name="codigoAdicional" minOccurs="0" type="codigoAdicional"/>
										<xsd:element name="descripcion" type="descripcion"/>
										<xsd:element name="cantidad" type="cantidad"/>
										<xsd:element name="precioUnitario" type="precioUnitario"/>
										<xsd:element name="descuento" minOccurs="0" type="descuento"/>
										<xsd:element name="precioTotalSinImpuesto" type="precioTotalSinImpuesto"/>
										<xsd:element name="detallesAdicionales" minOccurs="0">
											<xsd:complexType>
												<xsd:sequence>
												<xsd:element name="detAdicional" maxOccurs="3">
												<xsd:complexType>
												<xsd:attribute name="nombre">
												<xsd:simpleType>
												<xsd:restriction base="xsd:string">
												<xsd:minLength value="1"/>
												<xsd:maxLength value="300"/>
												</xsd:restriction>
												</xsd:simpleType>
												</xsd:attribute>
												<xsd:attribute name="valor">
												<xsd:simpleType>
												<xsd:restriction base="xsd:string">
												<xsd:pattern value="[^\\n]*"/>
												<xsd:minLength value="1"/>
												<xsd:maxLength value="300"/>
												</xsd:restriction>
												</xsd:simpleType>
												</xsd:attribute>
												</xsd:complexType>
												</xsd:element>
												</xsd:sequence>
											</xsd:complexType>
										</xsd:element>
										<xsd:element name="impuestos">
											<xsd:complexType>
												<xsd:sequence>
												<xsd:element name="impuesto" type="impuesto" minOccurs="0" maxOccurs="unbounded"/>
												</xsd:sequence>
											</xsd:complexType>
										</xsd:element>
									</xsd:sequence>
								</xsd:complexType>
							</xsd:element>
						</xsd:sequence>
					</xsd:complexType>
				</xsd:element>
				<xsd:element name="infoAdicional" minOccurs="0">
					<xsd:complexType>
						<xsd:sequence maxOccurs="1">
							<xsd:element name="campoAdicional" maxOccurs="15">
								<xsd:complexType>
									<xsd:simpleContent>
										<xsd:extension base="campoAdicional">
											<xsd:attribute name="nombre" type="nombre"/>
										</xsd:extension>
									</xsd:simpleContent>
								</xsd:complexType>
							</xsd:element>
						</xsd:sequence>
					</xsd:complexType>
				</xsd:element>
				<xsd:element ref="ds:Signature" minOccurs="0">
					<xsd:annotation>
						<xsd:documentation xml:lang="en"> Set of data associated with the invoice which guarantee the authorship and integrity of the message. It is defined as optional to ease the validation and transmission of the file. However, this block of electronic signature must be completed in order for an electronic invoice to be considered legally valid before third parties.</xsd:documentation>
						<xsd:documentation xml:lang="es"> Conjunto de datos asociados a la factura que garantizarán la autoría y la integridad del mensaje. Se define como opcional para facilitar la verificación y el tránsito del fichero. No obstante, debe cumplimentarse este bloque de firma electrónica para que se considere una factura electrónica válida legalmente frente a terceros.</xsd:documentation>
					</xsd:annotation>
				</xsd:element>
			</xsd:sequence>
			<xsd:attribute name="id" use="required">
				<xsd:simpleType>
					<xsd:restriction base="xsd:string">
						<xsd:enumeration value="comprobante"/>
					</xsd:restriction>
				</xsd:simpleType>
			</xsd:attribute>
			<xsd:attribute name="version" type="xsd:NMTOKEN" use="required"/>
		</xsd:complexType>
	</xsd:element>
	<xsd:element name="totalConImpuestos">
		<xsd:complexType>
			<xsd:sequence>
				<xsd:element maxOccurs="unbounded" name="totalImpuesto">
					<xsd:complexType>
						<xsd:sequence>
							<xsd:element name="codigo" type="codigo"/>
							<xsd:element name="codigoPorcentaje" type="codigoPorcentaje"/>
							<xsd:element name="baseImponible" minOccurs="1"  type="baseImponible"/>
							<xsd:element name="valor" minOccurs="1"  type="valor"/>
						</xsd:sequence>
					</xsd:complexType>
				</xsd:element>
			</xsd:sequence>
		</xsd:complexType>
	</xsd:element>
	<xsd:simpleType name="codDoc">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="dirMatriz">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaEmision">
		<xsd:restriction base="xsd:string">
			<xsd:pattern
				value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="dirEstablecimiento">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="contribuyenteEspecial">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="3"/>
			<xsd:maxLength value="13"/>
			<xsd:pattern value="([A-Za-z0-9])*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="obligadoContabilidad">
		<xsd:restriction base="xsd:string">
			<xsd:enumeration value="SI"/>
			<xsd:enumeration value="NO"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tipoIdentificacionComprador">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="13"/>
			<xsd:pattern value="[0][4-9]"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="razonSocialComprador">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="identificacionComprador">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="20"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigo">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]+"/>
			<xsd:minLength value="1"/>
			<xsd:maxLength value="1"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="totalSinImpuestos">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="baseImponible">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="moneda">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="15"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoPorcentaje">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]+"/>
			<xsd:minLength value="1"/>
			<xsd:maxLength value="4"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="valor">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="descripcion">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="cantidad">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="18"/>
			<xsd:fractionDigits value="6"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="precioUnitario">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="18"/>
			<xsd:fractionDigits value="6"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="descuento">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="precioTotalSinImpuesto">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tarifa">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="4"/>
			<xsd:fractionDigits value="2"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="nombre">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="campoAdicional">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
</xsd:schema>"""


XSD_SRI_110_GUIAREM = """<?xml version="1.1" encoding="UTF-8"?>
<!-- edited with XMLSPY v5 rel. 3 U (http://www.xmlspy.com) by ALEJANDRO SUBIA (SERVICIO DE RENTAS INTERNAS) -->
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
	xmlns:ns1="http://www.w3.org/2000/09/xmldsig#" elementFormDefault="qualified"
	attributeFormDefault="unqualified">
	<xsd:import namespace="http://www.w3.org/2000/09/xmldsig#"
		schemaLocation="http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd#"/>
	<xsd:simpleType name="numeroRuc">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero de RUC del Contribuyente</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{10}001"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="idCliente">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero de RUC Cedula o Pasaporte del Comprador</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="13"/>
			<xsd:pattern value="[0-9a-zA-Z]{0,13}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="numeroRucCedula">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero de RUC o cedula del Comprador</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="10"/>
			<xsd:maxLength value="13"/>
			<xsd:pattern value="[0-9]{10}"/>
			<xsd:pattern value="[0-9]{10}001"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fecha">
		<xsd:annotation>
			<xsd:documentation>Se detalla la fecha de uso del documento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaAutorizacion">
		<xsd:annotation>
			<xsd:documentation>Se detalla la fecha de la autorizacion</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaCaducidad">
		<xsd:annotation>
			<xsd:documentation>Se detalla la fecha de caducidad del documento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="establecimiento">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero del establecimiento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="puntoEmision">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero del punto de emision</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="secuencial">
		<xsd:annotation>
			<xsd:documentation>Se detalla el secuencial del documento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{9}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codTipoDoc">
		<xsd:annotation>
			<xsd:documentation>Se detalla el codigo del tipo de documento autorizado</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:integer">
			<xsd:maxInclusive value="6"/>
			<xsd:minInclusive value="6"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="documento">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero del documento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}-[0-9]{3}-[0-9]{1,9}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="autorizacion">
		<xsd:annotation>
			<xsd:documentation>Numero de autorizacion</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string"/>
	</xsd:simpleType>
	<xsd:simpleType name="claveAcceso">
		<xsd:annotation>
			<xsd:documentation>Corresponde al numero de autorizacion emitido por el sistema de Autorizacion de Comprobantes de Venta y Retencion
                    </xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{49}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codEstbDestino">
		<xsd:annotation>
			<xsd:documentation>Corresponde al codigo de establecimiento</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="docAduanero">
		<xsd:annotation>
			<xsd:documentation>Se detalla el numero de documento aduanero unico</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{13}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="ambiente">
		<xsd:annotation>
			<xsd:documentation>Desarrollo o produccion depende de en cual ambiente se genere el comprobante.</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[1-2]{1}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tipoEmision">
		<xsd:annotation>
			<xsd:documentation>Tipo de emision en el cual se genero el comprobante</xsd:documentation>
		</xsd:annotation>
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[12]{1}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="placa">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="20"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="dirDestinatario">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codDocSustento">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="numAutDocSustento">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{10,37}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaEmisionDocSustento">
		<xsd:restriction base="xsd:string">
			<xsd:pattern
				value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="numDocSustento">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{3}-[0-9]{3}-[0-9]{9}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="docAduaneroUnico">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="20"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="ruta">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="razonSocialDestinatario">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaFinTransporte">
		<xsd:restriction base="xsd:string">
			<xsd:pattern
				value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="dirPartida">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="fechaIniTRansporte">
		<xsd:restriction base="xsd:string">
			<xsd:pattern
				value="[0-9]{2}/[0-9]{2}/[0-9]{4}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:complexType name="infoTributaria">
		<xsd:annotation>
			<xsd:documentation>Contiene la informacion tributaria generica</xsd:documentation>
		</xsd:annotation>
		<xsd:sequence>
			<xsd:element name="ambiente" type="ambiente"/>
			<xsd:element name="tipoEmision" type="tipoEmision"/>
			<xsd:element name="razonSocial" type="razonSocial"/>
			<xsd:element name="nombreComercial" minOccurs="0" type="nombreComercial"/>
			<xsd:element name="ruc" type="numeroRuc"/>
			<xsd:element name="claveAcceso" type="claveAcceso"/>
			<xsd:element name="codDoc" type="codDoc"/>
			<xsd:element name="estab" type="establecimiento"/>
			<xsd:element name="ptoEmi" type="puntoEmision"/>
			<xsd:element name="secuencial" type="secuencial"/>
			<!--            <xsd:element name="docAduaneroUnico" type="numeroRucType" minOccurs="0"/>  -->
			<xsd:element name="dirMatriz" type="dirMatriz"/>
		</xsd:sequence>
	</xsd:complexType>
	<xsd:simpleType name="razonSocial">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="dirMatriz">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="dirEstablecimiento">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="totalSinImpuestos">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="contribuyenteEspecial">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="3"/>
			<xsd:maxLength value="13"/>
			<xsd:pattern value="([A-Za-z0-9])*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="obligadoContabilidad">
		<xsd:restriction base="xsd:string">
			<xsd:enumeration value="SI"/>
			<xsd:enumeration value="NO"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="nombreComercial">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tipoIdentificacionComprador">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0][4-7]"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="razonSocialTransportista">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="baseImponible">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="identificacionDestinatario">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="20"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="moneda">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="15"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigo">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{1}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoPorcentaje">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]"/>
			<xsd:minLength value="1"/>
			<xsd:maxLength value="4"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="motivoTraslado">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="rucTranportista">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[^\\n]*"/>
			<xsd:minLength value="1"/>
			<xsd:maxLength value="13"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="rise">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="40"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoInterno">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="25"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codigoAdicional">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="25"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="descripcion">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="cantidad">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="18"/>
			<xsd:fractionDigits value="6"/>
			<xsd:minInclusive value="0"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="valor">
		<xsd:restriction base="xsd:decimal">
			<xsd:totalDigits value="14"/>
			<xsd:fractionDigits value="2"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="codDoc">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0-9]{2}"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:complexType name="destinatario">
		<xsd:annotation>
			<xsd:documentation>Impuesto de una guia de remision.  Contiene los elementos de cada fila de la guia.</xsd:documentation>
		</xsd:annotation>
		<xsd:sequence>
			<xsd:element name="identificacionDestinatario" type="identificacionDestinatario" minOccurs="1"/>
			<xsd:element name="razonSocialDestinatario" type="razonSocialDestinatario"/>
			<xsd:element name="dirDestinatario" type="dirDestinatario"/>
			<xsd:element name="motivoTraslado" type="motivoTraslado"/>
			<xsd:element name="docAduaneroUnico" minOccurs="0" type="docAduaneroUnico"/>
			<xsd:element name="codEstabDestino" minOccurs="0" type="codEstbDestino"/>
			<xsd:element name="ruta" minOccurs="0" type="ruta"/>
			<xsd:element name="codDocSustento" minOccurs="0" type="codDocSustento"/>
			<xsd:element name="numDocSustento" minOccurs="0" type="numDocSustento"/>
			<xsd:element name="numAutDocSustento" minOccurs="0"  type="numAutDocSustento"/>
			<xsd:element name="fechaEmisionDocSustento" type="fechaEmisionDocSustento" minOccurs="0"/>
			<xsd:element name="detalles">
				<xsd:complexType>
					<xsd:sequence maxOccurs="unbounded">
						<xsd:element name="detalle" type="detalle"/>
					</xsd:sequence>
				</xsd:complexType>
			</xsd:element>
		</xsd:sequence>
	</xsd:complexType>
	<xsd:element name="guiaRemision">
		<xsd:annotation>
			<xsd:documentation>Elemento que describe una guia de remision</xsd:documentation>
		</xsd:annotation>
		<xsd:complexType>
			<xsd:sequence>
				<xsd:element name="infoTributaria" type="infoTributaria"/>
				<xsd:element name="infoGuiaRemision">
					<xsd:complexType>
						<xsd:sequence>
							<xsd:element name="dirEstablecimiento" minOccurs="0" type="dirEstablecimiento"/>
							<xsd:element name="dirPartida" type="dirPartida"/>
							<xsd:element name="razonSocialTransportista" type="razonSocialTransportista"/>
							<xsd:element name="tipoIdentificacionTransportista"	type="tipoIdentificacionTransportista"/>
							<xsd:element name="rucTransportista" type="rucTranportista"/>
							<xsd:element name="rise" minOccurs="0" type="rise"/>
							<xsd:element name="obligadoContabilidad" minOccurs="0" type="obligadoContabilidad"/>
							<xsd:element name="contribuyenteEspecial" minOccurs="0"	type="contribuyenteEspecial"/>
							<xsd:element name="fechaIniTransporte" type="fechaIniTRansporte"/>
							<xsd:element name="fechaFinTransporte" type="fechaFinTransporte"/>
							<xsd:element name="placa" type="placa"/>
						</xsd:sequence>
					</xsd:complexType>
				</xsd:element>
				<xsd:element name="destinatarios">
					<xsd:complexType>
						<xsd:sequence maxOccurs="unbounded">
							<xsd:element name="destinatario" type="destinatario"/>
						</xsd:sequence>
					</xsd:complexType>
				</xsd:element>
				<xsd:element name="infoAdicional" minOccurs="0">
					<xsd:complexType>
						<xsd:sequence maxOccurs="1">
							<xsd:element maxOccurs="15" name="campoAdicional">
								<xsd:complexType>
									<xsd:simpleContent>
										<xsd:extension base="campoAdicional">
											<xsd:attribute name="nombre" type="nombre"/>
										</xsd:extension>
									</xsd:simpleContent>
								</xsd:complexType>
							</xsd:element>
						</xsd:sequence>
					</xsd:complexType>
				</xsd:element>
				<xsd:element ref="ns1:Signature" minOccurs="0">
					<xsd:annotation>
						<xsd:documentation xml:lang="en"> Set of data associated with the invoice which guarantee the authorship and integrity of the message. It is defined as optional to ease the validation and transmission of the file. However, this block of electronic signature must be completed in order for an electronic invoice to be considered legally valid before third parties.</xsd:documentation>
						<xsd:documentation xml:lang="es"> Conjunto de datos asociados a la factura que garantizarán la autoría y la integridad del mensaje. Se define como opcional para facilitar la verificación y el tránsito del fichero. No obstante, debe cumplimentarse este bloque de firma electrónica para que se considere una factura electrónica válida legalmente frente a terceros.</xsd:documentation>
					</xsd:annotation>
				</xsd:element>
			</xsd:sequence>
			<xsd:attribute name="id" use="required">
				<xsd:simpleType>
					<xsd:restriction base="xsd:string">
						<xsd:enumeration value="comprobante"/>
					</xsd:restriction>
				</xsd:simpleType>
			</xsd:attribute>
			<xsd:attribute name="version" type="xsd:NMTOKEN" use="required"/>
		</xsd:complexType>
	</xsd:element>
	<xsd:complexType name="detalle">
		<xsd:annotation>
			<xsd:documentation>Detalle de una guia de remision.  Contiene los elementos de cada fila de la guia.</xsd:documentation>
		</xsd:annotation>
		<xsd:sequence>
			<xsd:element name="codigoInterno" minOccurs="0" type="codigoInterno"/>
			<xsd:element name="codigoAdicional" minOccurs="0" type="codigoAdicional"/>
			<xsd:element name="descripcion" type="descripcion"/>
			<xsd:element name="cantidad" type="cantidad"/>
			<xsd:element name="detallesAdicionales" minOccurs="0">
				<xsd:complexType>
					<xsd:sequence>
						<xsd:element name="detAdicional" minOccurs="0" maxOccurs="3">
							<xsd:complexType>
								<xsd:attribute name="nombre">
									<xsd:simpleType>
										<xsd:restriction base="xsd:string">
											<xsd:minLength value="1"/>
											<xsd:maxLength value="300"/>
											<xsd:pattern
												value="[^\\n]*"/>
										</xsd:restriction>
									</xsd:simpleType>
								</xsd:attribute>
								<xsd:attribute name="valor">
									<xsd:simpleType>
										<xsd:restriction base="xsd:string">
											<xsd:pattern
												value="[^\\n]*"/>
											<xsd:minLength value="1"/>
											<xsd:maxLength value="300"/>
										</xsd:restriction>
									</xsd:simpleType>
								</xsd:attribute>
							</xsd:complexType>
						</xsd:element>
					</xsd:sequence>
				</xsd:complexType>
			</xsd:element>
		</xsd:sequence>
	</xsd:complexType>
	<xsd:simpleType name="nombre">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="campoAdicional">
		<xsd:restriction base="xsd:string">
			<xsd:minLength value="1"/>
			<xsd:maxLength value="300"/>
			<xsd:pattern value="[^\\n]*"/>
		</xsd:restriction>
	</xsd:simpleType>
	<xsd:simpleType name="tipoIdentificacionTransportista">
		<xsd:restriction base="xsd:string">
			<xsd:pattern value="[0][4-7]"/>
		</xsd:restriction>
	</xsd:simpleType>
</xsd:schema>"""


def validate_doc(xml_content, xsd_content):
    u"""
    Dado un contenido XML de entrada, y un contenido XSD de validacion XML.
    Dado una funcion de validacion semantica (algo de lo que un XSD no se puede encargar).
    Primero ocurre una validacion a nivel XML/XSD.
    TODO
        Crear una validación semántica.
    """

    try:
        root = etree.XML(xml_content.strip())
    except Exception as e:
        raise XMLFormatException(str(e), XMLFormatException.IN_XML)

    try:
        schema = etree.XMLSchema(etree.XML(xsd_content.strip()))
    except Exception as e:
        raise XMLFormatException(str(e), XMLFormatException.IN_XSD)

    if not schema.validate(root):
        raise XMLValidationException("Se produjo un error al validar el XML", schema.error_log)

