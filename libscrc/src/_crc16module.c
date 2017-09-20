/*
*********************************************************************************************************
*                              		(c) Copyright 2006-2017, HZ, Studio
*                                           All Rights Reserved
* File    : _crc16module.c
* Author  : Heyn (heyunhuan@gmail.com)
* Version : V0.1.2
* Web	  : http://heyunhuan513.blog.163.com
*
* LICENSING TERMS:
* ---------------
*		New Create at 	2017-08-09 09:52AM
*                       2017-08-17 [Heyn] Optimized Code.
*                                         Wheel 0.0.4 New CRC16-SICK / CRC16-DNP
*                       2017-08-21 [Heyn] Optimization code for the C99 standard.
*                                         for ( unsigned int i=0; i<256; i++ ) -> for ( i=0; i<256; i++ )
*                       2017-08-22 [Heyn] Bugfixes Parsing arguments
*                                           Change PyArg_ParseTuple(* , "y#|I")
*                                           To     PyArg_ParseTuple(* , "y#|H")
*                                           "H" : Convert a Python integer to a C unsigned short int,
*                                               without overflow checking.
*                       2017-09-19 [Heyn] New CRC16-X25. (V0.1.1)
*                                         Bugfies 
*                                           Change  crc = hz_update_crc16_kermit(crc16, pSrc[i]);
*                                           TO     crc = hz_update_crc16_kermit(crc, pSrc[i]);
*                                         Optimized Code.
*
*********************************************************************************************************
*/

#include <Python.h>
#include "_crc16tables.h"

#define                 TRUE                    1
#define                 FALSE                   0

#define                 HZ16_POLYNOMIAL_A001    0xA001
#define                 HZ16_POLYNOMIAL_8005    0x8005
#define                 HZ16_POLYNOMIAL_DNP     0xA6BC

static int              crc_tab16_a001_init     = FALSE;
static int              crc_tab16_8005_init     = FALSE;
static int              crc_tab16_dnp_init      = FALSE;

static unsigned short   crc_tab16_a001[256]     = {0x0000};
static unsigned short   crc_tab16_8005[256]     = {0x0000};
static unsigned short   crc_tab16_dnp[256]      = {0x0000};


/*
*********************************************************************************************************
                                    POLY=0xA001 [Modbus]
*********************************************************************************************************
*/

void init_crc16_a001_table( void ) 
{
    unsigned int i = 0, j = 0;
    unsigned short crc, c;

    for ( i=0; i<256; i++ ) {
        crc = 0;
        c   = (unsigned short) i;
        for ( j=0; j<8; j++ ) {
            if ( (crc ^ c) & 0x0001 ) {
                crc = ( crc >> 1 ) ^ HZ16_POLYNOMIAL_A001;
            } else {
                crc =   crc >> 1;
            }
            c = c >> 1;
        }
        crc_tab16_a001[i] = crc;
    }
    crc_tab16_a001_init = TRUE;
}

unsigned short hz_update_crc16_a001( unsigned short crc16, unsigned char c ) 
{
    unsigned short crc = crc16;
    unsigned short tmp, short_c;

    short_c = 0x00FF & (unsigned short) c;
    if ( ! crc_tab16_a001_init ) init_crc16_a001_table();

    tmp =  crc       ^ short_c;
    crc = (crc >> 8) ^ crc_tab16_a001[ tmp & 0xFF ];

    return crc;
}

/*
 * Width            = 16
 * Poly             = 0xA001
 * InitValue(crc16) = 0xFFFF or 0x0000
 */
unsigned short hz_calc_crc16_a001( const unsigned char *pSrc, unsigned int len, unsigned short crc16 )
{
    unsigned int i = 0;
    unsigned short crc = crc16;

	for ( i=0; i<len; i++ ) {
		crc = hz_update_crc16_a001(crc, pSrc[i]);
	}
	return crc;
}

/*
 *
 */
static PyObject * _crc16_modbus(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00000000L;
    unsigned short crc16  = 0xFFFF;
    unsigned short result = 0x0000;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|H", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|H", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc16_a001(data, data_len, crc16);

    return Py_BuildValue("H", result);
}

/*
*********************************************************************************************************
                                    POLY=0x8005 [IBM]
*********************************************************************************************************
*/
void init_crc16_8005_table( void ) 
{
    unsigned int i = 0, j = 0;
    unsigned short crc, c;

    for ( i=0; i<256; i++ ) {
        crc = 0;
        c   = (unsigned short) i << 8;
        for ( j=0; j<8; j++ ) {
            if ( (crc ^ c) & 0x8000 ) {
                crc = ( crc << 1 ) ^ HZ16_POLYNOMIAL_8005;
            } else {
                crc =   crc << 1;
            }
            c = c << 1;
        }
        crc_tab16_8005[i] = crc;
    }
    crc_tab16_8005_init = TRUE;
}

unsigned short hz_update_crc16_8005( unsigned short crc16, unsigned char c ) 
{
    unsigned short crc = crc16;
    unsigned short tmp, short_c;

    short_c = 0x00FF & (unsigned short) c;

    if ( ! crc_tab16_8005_init ) init_crc16_8005_table();

    tmp = (crc >> 8) ^ short_c;
    crc = (crc << 8) ^ crc_tab16_8005[tmp];
    return crc;

}

/*
 * Width        = 16
 * Poly         = 0x8005
 * InitValue    = 0x0000
 */
unsigned short hz_calc_crc16_ibm( const unsigned char *pSrc, unsigned int len, unsigned short crc16 )
{
    unsigned int i = 0;
    unsigned short crc = crc16;

	for ( i=0; i<len; i++ ) {
		crc = hz_update_crc16_8005(crc,pSrc[i]);
	}
	return crc;
}

/*
 *
 */
static PyObject * _crc16_ibm(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00000000L;
    unsigned short crc16  = 0x0000;
    unsigned short result = 0x0000;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|H", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|H", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc16_ibm(data, data_len, crc16);

    return Py_BuildValue("H", result);
}

/*
*********************************************************************************************************
                                    POLY=0x1021 [CCITT XModem]
*********************************************************************************************************
*/

static PyObject * _crc16_xmodem(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00000000L;
    unsigned short crc16  = 0x0000;
    unsigned short result = 0x0000;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|H", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|H", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc16_l1021(data, data_len, crc16);

    return Py_BuildValue("H", result);
}

static PyObject * _crc16_ccitt(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00000000L;
    unsigned short crc16  = 0xFFFF;
    unsigned short result = 0x0000;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|H", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|H", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc16_l1021(data, data_len, crc16);

    return Py_BuildValue("H", result);
}

/*
*********************************************************************************************************
                                    POLY=0x8408 [Kermit]
*********************************************************************************************************
*/

static PyObject * _crc16_kermit(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00000000L;
    unsigned short crc16  = 0x0000;
    unsigned short result = 0x0000;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|H", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|H", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc16_r8408(data, data_len, crc16);

    return Py_BuildValue("H", result);
}

/*
*********************************************************************************************************
                                    POLY=0x1021 [X25]
*********************************************************************************************************
*/
static PyObject * _crc16_x25(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00000000L;
    unsigned short crc16  = 0xFFFF;
    unsigned short result = 0x0000;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|H", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|H", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc16_r8408(data, data_len, crc16);
    result = ~result;
    return Py_BuildValue("H", result);
}

/*
*********************************************************************************************************
                                    POLY=0x8005 [SICK]
*********************************************************************************************************
*/

unsigned short hz_update_crc16_sick( unsigned short crc16, unsigned char c, char prev_byte ) 
{
    unsigned short crc = crc16;
    unsigned short short_c, short_p;

    short_c  =   0x00FF & (unsigned short) c;
    short_p  = ( 0x00FF & (unsigned short) prev_byte ) << 8;

    if ( crc & 0x8000 ) crc = ( crc << 1 ) ^ HZ16_POLYNOMIAL_8005;
    else                crc =   crc << 1;

    crc &= 0xFFFF;
    crc ^= ( short_c | short_p );

    return crc;
}

unsigned short hz_calc_crc16_sick( const unsigned char *pSrc, unsigned int len, unsigned short crc16 )
{
    unsigned int   i            = 0;
			 char  prev_byte	= 0x00;
	unsigned short crc		    = crc16;

	for ( i=0; i<len; i++ ) {
		crc	        = hz_update_crc16_sick(crc, pSrc[i], prev_byte);
		prev_byte	= pSrc[i];
    }

	return crc;
}

static PyObject * _crc16_sick(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00000000L;
    unsigned short crc16  = 0x0000;
    unsigned short result = 0x0000;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|H", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|H", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc16_sick(data, data_len, crc16);

    return Py_BuildValue("H", result);
}

/*
*********************************************************************************************************
                                    POLY=0xA6BC [DNP]
*********************************************************************************************************
*/

void init_crc16_dnp_tab( void ) 
{
    unsigned int i = 0, j = 0;
    unsigned short crc, c;

    for ( i=0; i<256; i++ ) {
        crc = 0;
        c   = (unsigned short) i;
        for ( j=0; j<8; j++ ) {
            if ( (crc ^ c) & 0x0001 ) crc = ( crc >> 1 ) ^ HZ16_POLYNOMIAL_DNP;
            else                      crc =   crc >> 1;
            c = c >> 1;
        }
        crc_tab16_dnp[i] = crc;
    }
    crc_tab16_dnp_init = TRUE;
}

unsigned short hz_update_crc16_dnp( unsigned short crc16, unsigned char c ) 
{
    unsigned short crc = crc16;
    unsigned short tmp, short_c;

    short_c = 0x00FF & (unsigned short) c;

    if ( ! crc_tab16_dnp_init ) init_crc16_dnp_tab();

    tmp =  crc       ^ short_c;
    crc = (crc >> 8) ^ crc_tab16_dnp[ tmp & 0xFF ];

    return crc;
}

unsigned short hz_calc_crc16_dnp( const unsigned char *pSrc, unsigned int len, unsigned short crc16)
{
    unsigned int i = 0;
	unsigned short crc = crc16;
    
    for ( i=0; i<len; i++ ) {
        crc	= hz_update_crc16_dnp(crc, pSrc[i]);
    }
    return ~crc;
}

static PyObject * _crc16_dnp(PyObject *self, PyObject *args)
{
    const unsigned char *data = NULL;
    unsigned int data_len = 0x00000000L;
    unsigned short crc16  = 0x0000;
    unsigned short result = 0x0000;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|H", &data, &data_len, &crc16))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|H", &data, &data_len, &crc16))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc16_dnp(data, data_len, crc16);

    return Py_BuildValue("H", result);
}


/* method table */
static PyMethodDef _crc16Methods[] = {
    {"modbus",  _crc16_modbus, METH_VARARGS, "Calculate Modbus of CRC16              [Poly=0xA001, Init=0xFFFF Xorout=0x0000 Refin=True Refout=True]"},
    {"ibm",     _crc16_ibm,    METH_VARARGS, "Calculate IBM (Alias:ARC/LHA) of CRC16 [Poly=0x8005, Init=0x0000 Xorout=0xFFFF Refin=True Refout=True]"},
    {"xmodem",  _crc16_xmodem, METH_VARARGS, "Calculate XMODEM of CRC16              [Poly=0x1021, Init=0x0000 Xorout=0x0000 Refin=False Refout=False]"},
    {"ccitt",   _crc16_ccitt,  METH_VARARGS, "Calculate CCITT-FALSE of CRC16         [Poly=0x1021, Init=0xFFFF or 0x1D0F]"},
    {"kermit",  _crc16_kermit, METH_VARARGS, "Calculate Kermit of CRC16              [Poly=0x8408, Init=0x0000]"},
    {"sick",    _crc16_sick,   METH_VARARGS, "Calculate Sick of CRC16                [Poly=0x8005, Init=0x0000]"},
    {"dnp",     _crc16_dnp,    METH_VARARGS, "Calculate DNP (Ues:M-Bus)  of CRC16    [Poly=0x3D65, Init=0x0000 Xorout=0xFFFF Refin=True Refout=True]"},
    {"x25",     _crc16_x25,    METH_VARARGS, "Calculate X25  of CRC16                [Poly=0x1021, Init=0xFFFF Xorout=0xFFFF Refin=True Refout=True]"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


/* module documentation */
PyDoc_STRVAR(_crc16_doc,
"Calculation of CRC16 \n"
"Modbus IBM CCITT-XMODEM CCITT-KERMIT CCITT-0xFFFF CCITT-0x1D0F \n"
"CRC16-SICK CRC16-DNP CRC16-X25\n"
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

    PyModule_AddStringConstant(m, "__version__", "0.1.2");
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
