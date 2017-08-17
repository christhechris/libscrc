/*
*********************************************************************************************************
*                              		(c) Copyright 2006-2017, HZ, Studio
*                                           All Rights Reserved
* File    : _crc8module.c
* Author  : Heyn (heyunhuan@gmail.com)
* Version : V0.0.3
* Web	  : http://heyunhuan513.blog.163.com
*
* LICENSING TERMS:
* ---------------
*		New Create at 	2017-08-10 08:42AM
*                       2017-08-17 [Heyn] Optimized Code.
*
*********************************************************************************************************
*/

#include <Python.h>

#define                 TRUE                    1
#define                 FALSE                   0

static int              crc_tab8_verb_init      = FALSE;
static unsigned char	crc_tab8_verb[256]      = {0x00};


/*
 * Width            = 8
 * InitValue(crc8)  = 0x00
 */
unsigned char hz_calc_crc8_bcc( const unsigned char *pSrc, unsigned int len, unsigned char crc8 ) 
{
    unsigned char crc = crc8;

	for ( unsigned int i=0; i<len; i++ ) {
		crc ^= pSrc[i];
    }

	return crc;
}

/*
 * Width            = 8
 * InitValue(crc8)  = 0x00
 */
unsigned char hz_calc_crc8_lrc( const unsigned char *pSrc, unsigned int len, unsigned char crc8 ) 
{
    unsigned char crc = crc8;

	for ( unsigned int i=0; i<len; i++ ) {
		crc += pSrc[i];
	}
    crc = (~crc) + 0x01;

	return crc;
}

void init_crc8_verb_table(void)
{
    unsigned char crc, c;

    for ( unsigned int i=0; i<256; i++ ) {
        crc = 0;
        c   = i;
        for ( unsigned int j=0; j<8; j++ ) {
			if ((crc ^ c) & 0x01) {
				crc = crc >> 0x01;
				crc = crc ^ 0x8C;
			} else {
				crc = crc >> 0x01;
			}
			c = c >> 0x01;
        }
        crc_tab8_verb[i] = crc;
    }
	crc_tab8_verb_init = TRUE;
}

unsigned char hz_update_crc8_verb( unsigned char crc8, unsigned char c ) 
{
    unsigned char crc = crc8;
    if ( ! crc_tab8_verb_init ) init_crc8_verb_table();
    crc = crc_tab8_verb[ crc ^ c ];
    return crc;
}

unsigned char hz_calc_crc8_verb( const unsigned char *pSrc, unsigned int len, unsigned char crc8 ) 
{
    unsigned char crc = crc8;
	for ( unsigned int i=0; i<len; i++ ) {
		crc = hz_update_crc8_verb(crc, pSrc[i]);
	}
	return crc;
}


static PyObject * _crc8_intel(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00;
    unsigned char crc8    = 0x00;
    unsigned char result  = 0x00;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|I", &data, &data_len, &crc8))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|I", &data, &data_len, &crc8))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc8_lrc(data, data_len, crc8);

    return Py_BuildValue("B", result);
}

static PyObject * _crc8_bcc(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00;
    unsigned char crc8    = 0x00;
    unsigned char result  = 0x00;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|I", &data, &data_len, &crc8))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|I", &data, &data_len, &crc8))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc8_bcc(data, data_len, crc8);

    return Py_BuildValue("B", result);
}

static PyObject * _crc8_lrc(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00;
    unsigned char crc8    = 0x00;
    unsigned char result  = 0x00;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|I", &data, &data_len, &crc8))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|I", &data, &data_len, &crc8))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc8_lrc(data, data_len, crc8);

    return Py_BuildValue("B", result);
}

static PyObject * _crc8_verb(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00;
    unsigned char crc8    = 0x00;
    unsigned char result  = 0x00;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|I", &data, &data_len, &crc8))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|I", &data, &data_len, &crc8))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc8_verb(data, data_len, crc8);

    return Py_BuildValue("B", result);
}

/* method table */
static PyMethodDef _crc8Methods[] = {
    {"intel",   _crc8_intel,    METH_VARARGS, "Calculate Intel hexadecimal of CRC8 [Initial = 0x00]"},
    {"bcc",     _crc8_bcc,      METH_VARARGS, "Calculate BCC of CRC8 [Initial = 0x00]"},
    {"lrc",     _crc8_lrc,      METH_VARARGS, "Calculate LRC of CRC8 [Initial = 0x00]"},
    {"verb",    _crc8_verb,     METH_VARARGS, "Calculate Verb of CRC8 [Poly = 0x8C Initial = 0x00] for DS18B20"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


/* module documentation */
PyDoc_STRVAR(_crc8_doc,
"Calculation of CRC8 \n"
"libscrc.intel -> Calculate Intel hexadecimal of CRC8 [Initial = 0x00]\n"
"libscrc.bcc   -> Calculate BCC(XOR) of CRC8 [Initial = 0x00]\n"
"libscrc.lrc   -> Calculate LRC of CRC8 [Initial = 0x00]\n"
"libscrc.verb  -> Calculate DS18B20 of CRC8 [Poly = 0x8C Initial = 0x00]\n"
"\n");


#if PY_MAJOR_VERSION >= 3

/* module definition structure */
static struct PyModuleDef _crc8module = {
   PyModuleDef_HEAD_INIT,
   "_crc8",                    /* name of module */
   _crc8_doc,                  /* module documentation, may be NULL */
   -1,                         /* size of per-interpreter state of the module */
   _crc8Methods
};

/* initialization function for Python 3 */
PyMODINIT_FUNC
PyInit__crc8(void)
{
    PyObject *m = NULL;

    m = PyModule_Create(&_crc8module);
    if (m == NULL) {
        return NULL;
    }

    PyModule_AddStringConstant(m, "__version__", "0.0.3");
    PyModule_AddStringConstant(m, "__author__",  "Heyn");

    return m;
}

#else

/* initialization function for Python 2 */
PyMODINIT_FUNC
init_crc8(void)
{
    (void) Py_InitModule3("_crc8", _crc8Methods, _crc8_doc);
}

#endif /* PY_MAJOR_VERSION */
