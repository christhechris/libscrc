/*
*********************************************************************************************************
*                              		(c) Copyright 2006-2017, HZ, Studio
*                                           All Rights Reserved
* File    : _crc16module.c
* Author  : Heyn (heyunhuan@gmail.com)
* Version : V0.0.1
* Web	  : http://heyunhuan513.blog.163.com
*
* LICENSING TERMS:
* ---------------
*		New Create at 	2017-08-09 09:52AM
*
*********************************************************************************************************
*/

#include <Python.h>

#define             TRUE                    1
#define             FALSE                   0

#define		        HZ16_POLYNOMIAL_A001	0xA001
#define	    	    HZ16_POLYNOMIAL_8005    0x8005
#define		        HZ16_POLYNOMIAL_CCITT	0x1021
#define		        HZ16_POLYNOMIAL_KERMIT	0x8408


static int          crc_tab16_a001_init     = FALSE;
static int          crc_tab16_8005_init     = FALSE;
static int          crc_tab16_ccitt_init    = FALSE;
static int          crc_tab16_kermit_init   = FALSE;


static unsigned short		crc_tab16_a001[256]     = {0x0000};
static unsigned short		crc_tab16_8005[256]     = {0x0000};
static unsigned short		crc_tab16_ccitt[256]    = {0x0000};
static unsigned short		crc_tab16_kermit[256]   = {0x0000};

/*
*********************************************************************************************************
                                    POLY=0xA001 [Modbus]
*********************************************************************************************************
*/
void init_crc16_a001_table( void ) 
{
    int i, j;
    unsigned short crc, c;

    for (i=0; i<256; i++) {
        crc = 0;
        c   = (unsigned short) i;
        for (j=0; j<8; j++) {
            if ( (crc ^ c) & 0x0001 ) crc = ( crc >> 1 ) ^ HZ16_POLYNOMIAL_A001;
            else                      crc =   crc >> 1;
            c = c >> 1;
        }
        crc_tab16_a001[i] = crc;
    }
    crc_tab16_a001_init = TRUE;
}

unsigned short hz_update_crc16_a001( unsigned short crc16, unsigned char c ) 
{
    unsigned short tmp, short_c;

    short_c = 0x00FF & (unsigned short) c;
    if ( ! crc_tab16_a001_init ) init_crc16_a001_table();

    tmp   =  crc16       ^ short_c;
    crc16 = (crc16 >> 8) ^ crc_tab16_a001[ tmp & 0xFF ];

    return crc16;
}

/*
 * Width            = 16
 * Poly             = 0xA001
 * InitValue(crc16) = 0xFFFF or 0x0000
 */
unsigned short hz_calc_crc16_a001( unsigned char *pSrc, unsigned int len, unsigned short crc16 )
{
	for (unsigned int i=0; i<len; i++) {
		crc16 = hz_update_crc16_a001(crc16, pSrc[i]);
	}
	return crc16;
}

/*
 *
 */
static PyObject * _crc16_modbus(PyObject *self, PyObject *args)
{
    const unsigned char* data;
    unsigned int data_len;
    unsigned short crc16 = 0xFFFF;
    unsigned short result;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|I:modbus", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|I:modbus", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc16_a001(data, data_len, crc16);

    return Py_BuildValue("I", result);
}

/*
*********************************************************************************************************
                                    POLY=0x8005 [IBM]
*********************************************************************************************************
*/
void init_crc16_8005_table( void ) 
{
    int i, j;
    unsigned short crc, c;

    for (i=0; i<256; i++) {
        crc = 0;
        c   = (unsigned short) i << 8;
        for (j=0; j<8; j++) {
            if ( (crc ^ c) & 0x8000 ) crc = ( crc << 1 ) ^ HZ16_POLYNOMIAL_8005;
            else                      crc =   crc << 1;
            c = c << 1;
        }
        crc_tab16_8005[i] = crc;
    }
    crc_tab16_8005_init = TRUE;
}

unsigned short hz_update_crc16_8005( unsigned short crc16, unsigned char c ) 
{

    unsigned short tmp, short_c;

    short_c = 0x00ff & (unsigned short) c;

    if ( ! crc_tab16_8005_init ) init_crc16_8005_table();

    tmp = (crc16 >> 8) ^ short_c;
    crc16 = (crc16 << 8) ^ crc_tab16_8005[tmp];
    return crc16;

}

/*
 * Width        = 16
 * Poly         = 0x8005
 * InitValue    = 0x0000
 */
unsigned short hz_calc_crc16_ibm( unsigned char *pSrc, unsigned int len, unsigned short crc16 )
{
	for (unsigned int i=0; i<len; i++) {
		crc16 = hz_update_crc16_8005(crc16,pSrc[i]);
	}
	return crc16;
}

/*
 *
 */
static PyObject * _crc16_ibm(PyObject *self, PyObject *args)
{
    const unsigned char* data;
    unsigned int data_len;
    unsigned short crc16 = 0;
    unsigned short result;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|I:ibm", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|I:ibm", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc16_ibm(data, data_len, crc16);

    return Py_BuildValue("I", result);
}

/*
*********************************************************************************************************
                                    POLY=0x1021 [CCITT XModem]
*********************************************************************************************************
*/
void init_crc16_ccitt_table( void ) 
{
    int i, j;
    unsigned short crc, c;

    for (i=0; i<256; i++) {
        crc = 0;
        c   = ((unsigned short) i) << 8;
        for (j=0; j<8; j++) {
            if ( (crc ^ c) & 0x8000 ) crc = ( crc << 1 ) ^ HZ16_POLYNOMIAL_CCITT;
            else                      crc =   crc << 1;
            c = c << 1;
        }
        crc_tab16_ccitt[i] = crc;
    }
    crc_tab16_ccitt_init = TRUE;
}

unsigned short hz_update_crc16_ccitt( unsigned short crc16, unsigned char c ) {

    unsigned short tmp, short_c;

    short_c  = 0x00ff & (unsigned short) c;

    if ( ! crc_tab16_ccitt_init ) init_crc16_ccitt_table();

    tmp = (crc16 >> 8) ^ short_c;
    crc16 = (crc16 << 8) ^ crc_tab16_ccitt[tmp];

    return crc16;

}

unsigned short hz_calc_ccitt( unsigned char *pSrc, unsigned int len, unsigned short crc16)
{
	for (unsigned int i=0; i<len; i++) {
		crc16 = hz_update_crc16_ccitt(crc16, pSrc[i]);
	}
	return crc16;
}

static PyObject * _crc16_xmodem(PyObject *self, PyObject *args)
{
    const unsigned char* data;
    unsigned int data_len;
    unsigned short crc16 = 0x0000;
    unsigned short result;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|I:xmodem", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|I:xmodem", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_ccitt(data, data_len, crc16);

    return Py_BuildValue("I", result);
}

static PyObject * _crc16_ccitt(PyObject *self, PyObject *args)
{
    const unsigned char* data;
    unsigned int data_len;
    unsigned short crc16 = 0xFFFF;
    unsigned short result;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|I:ccitt", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|I:ccitt", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_ccitt(data, data_len, crc16);

    return Py_BuildValue("I", result);
}

/*
*********************************************************************************************************
                                    POLY=0x8408 [CCITT Kermit]
*********************************************************************************************************
*/
void init_crc16_kermit_table( void ) 
{
    int i, j;
    unsigned short crc, c;

    for (i=0; i<256; i++) {
        crc = 0;
        c   = (unsigned short) i;
        for (j=0; j<8; j++) {
            if ( (crc ^ c) & 0x0001 ) crc = ( crc >> 1 ) ^ HZ16_POLYNOMIAL_KERMIT;
            else                      crc =   crc >> 1;
            c = c >> 1;
        }
        crc_tab16_kermit[i] = crc;
    }
    crc_tab16_kermit_init = TRUE;
}

unsigned short hz_update_crc16_kermit( unsigned short crc, unsigned char c ) 
{
    unsigned short tmp, short_c;

    short_c = 0x00ff & (unsigned short) c;
    if ( ! crc_tab16_kermit_init ) init_crc16_kermit_table();

    tmp =  crc       ^ short_c;
    crc = (crc >> 8) ^ crc_tab16_kermit[ tmp & 0xff ];

    return crc;
}

unsigned short hz_calc_ccitt_kermit( unsigned char *pSrc, unsigned int len, unsigned short crc16 )
{
	for (unsigned int i=0; i<len; i++) {
		crc16	= hz_update_crc16_kermit(crc16, pSrc[i]);
	}
	return crc16;
}

static PyObject * _crc16_kermit(PyObject *self, PyObject *args)
{
    const unsigned char* data;
    unsigned int data_len;
    unsigned short crc16 = 0x0000;
    unsigned short result;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|I:kermit", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|I:kermit", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_ccitt_kermit(data, data_len, crc16);

    return Py_BuildValue("I", result);
}



/* method table */
static PyMethodDef _crc16Methods[] = {
    {"modbus",  _crc16_modbus, METH_VARARGS, "Calculate CRC (Modbus) of CRC16 [Poly=0xA001, Init=0xFFFF]"},
    {"ibm",     _crc16_ibm,    METH_VARARGS, "Calculate CRC (IBM/ARC/LHA) of CRC16 [Poly=0x8005, Init=0x0000]"},
    {"xmodem",  _crc16_xmodem, METH_VARARGS, "Calculate CCITT CRC16  [Poly=0x1021 Init=0x0000)"},
    {"ccitt",   _crc16_ccitt,  METH_VARARGS, "Calculate CCITT CRC16  [Poly=0x1021 Init=0xFFFF or 0x1D0F)"},
    {"kermit",  _crc16_kermit, METH_VARARGS, "Calculate Kermit CRC16 [Poly=0x8408 Init=0x0000)"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


/* module documentation */
PyDoc_STRVAR(_crc16_doc,
"Calculation of CRC16 \n"
"Modbus IBM CCITT-XMODEM CCITT-KERMIT CCITT-0xFFFF CCITT-0x1D0F\n"
"\n");


#if PY_MAJOR_VERSION >= 3

/* module definition structure */
static struct PyModuleDef _crc16module = {
   PyModuleDef_HEAD_INIT,
   "_crc16",                    /* name of module */
   _crc16_doc,                  /* module documentation, may be NULL */
   -1,                          /* size of per-interpreter state of the module */
   _crc16Methods
};

/* initialization function for Python 3 */
PyMODINIT_FUNC
PyInit__crc16(void)
{
    PyObject *m;

    m = PyModule_Create(&_crc16module);
    if (m == NULL) {
        return NULL;
    }

    PyModule_AddStringConstant(m, "__version__", "0.0.1");
    PyModule_AddStringConstant(m, "__author__", "Heyn");

    return m;
}

#else

/* initialization function for Python 2 */
PyMODINIT_FUNC
init_crc16(void)
{
    (void) Py_InitModule3("_crc16", _crc16Methods, _crc16_doc);
}

#endif /* PY_MAJOR_VERSION */
