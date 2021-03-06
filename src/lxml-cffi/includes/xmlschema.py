import cffi
from . import tree, xmlerror, xmlparser

ffi = cffi.FFI()
ffi.include(xmlerror.ffi)
ffi.include(tree.ffi)
ffi.include(xmlparser.ffi)
ffi.cdef("""
    typedef struct _xmlSchemaParserCtxt xmlSchemaParserCtxt;
    typedef xmlSchemaParserCtxt *xmlSchemaParserCtxtPtr;

    typedef struct _xmlSchemaValidCtxt xmlSchemaValidCtxt;
    typedef xmlSchemaValidCtxt *xmlSchemaValidCtxtPtr;

    typedef struct _xmlSchema xmlSchema;
    typedef xmlSchema *xmlSchemaPtr;

    typedef enum {
        XML_SCHEMA_VAL_VC_I_CREATE = 1
            /* Default/fixed: create an attribute node
            * or an element's text node on the instance.
            */
    } xmlSchemaValidOption;

    xmlSchemaParserCtxtPtr xmlSchemaNewParserCtxt	(const char *URL);
    xmlSchemaParserCtxtPtr xmlSchemaNewDocParserCtxt	(xmlDocPtr doc);
    void    xmlSchemaFreeParserCtxt	(xmlSchemaParserCtxtPtr ctxt);

    void    xmlSchemaSetParserStructuredErrors(xmlSchemaParserCtxtPtr ctxt,
					 xmlStructuredErrorFunc serror,
					 void *ctx);
    xmlSchemaPtr xmlSchemaParse		(xmlSchemaParserCtxtPtr ctxt);
    void    xmlSchemaFree		(xmlSchemaPtr schema);

    xmlSchemaValidCtxtPtr xmlSchemaNewValidCtxt	(xmlSchemaPtr schema);
    void    xmlSchemaSetValidStructuredErrors(xmlSchemaValidCtxtPtr ctxt,
					 xmlStructuredErrorFunc serror,
					 void *ctx);
    int     xmlSchemaSetValidOptions	(xmlSchemaValidCtxtPtr ctxt,
					 int options);
    int 	xmlSchemaIsValid	(xmlSchemaValidCtxtPtr ctxt);
    int     xmlSchemaValidateDoc	(xmlSchemaValidCtxtPtr ctxt,
					 xmlDocPtr instance);
    void    xmlSchemaFreeValidCtxt	(xmlSchemaValidCtxtPtr ctxt);

    /* Interface to insert Schemas SAX validation in a SAX stream */
    typedef struct _xmlSchemaSAXPlug xmlSchemaSAXPlugStruct;
    typedef xmlSchemaSAXPlugStruct *xmlSchemaSAXPlugPtr;
    xmlSchemaSAXPlugPtr xmlSchemaSAXPlug(xmlSchemaValidCtxtPtr ctxt,
					 xmlSAXHandlerPtr *sax,
					 void **user_data);
    int     xmlSchemaSAXUnplug		(xmlSchemaSAXPlugPtr plug);

""")

libxml = ffi.verify("""
    #include "libxml/xmlschemas.h"
""",
include_dirs=['/usr/include/libxml2'],
libraries=['xml2'])

def init():
    for name in dir(libxml):
        if name.startswith(('xml', 'XML')):
            globals()[name] = getattr(libxml, name)

init()
