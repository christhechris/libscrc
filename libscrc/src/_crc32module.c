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
*		New Create at 	2017-08-09 16:39PM
*
*********************************************************************************************************
*/

#include <Python.h>

#define                 TRUE                    1
#define                 FALSE                   0

#define		            HZ32_POLYNOMIAL_FSC		0x04C11DB7L
#define		            HZ32_POLYNOMIAL_CRC		0xEDB88320L

static int              crc_tab32_fsc_init      = FALSE;
static int              crc_tab32_crc_init      = FALSE;

static unsigned long	crc_tab32_fsc[256]      = {0x00000000};
static unsigned long    crc_tab32_crc[256]      = {0x00000000};


/*
*********************************************************************************************************
                                    POLY=0x04C11DB7L [FSC]
*********************************************************************************************************
*/

void init_crc32_fsc_table( void ) 
{
    int i, j;
    unsigned int crc,c;

    for (i=0; i<256; i++) {
		crc = 0;
		c	= ((unsigned int ) i) << 24;
        for (j=0; j<8; j++) {
            if ( (crc ^ c) & 0x80000000L )	crc = ( crc << 1 ) ^ HZ32_POLYNOMIAL_FSC;
            else							crc =   crc << 1;
			c = c << 1;

        }
        crc_tab32_fsc[i] = crc;
    }
    crc_tab32_fsc_init = TRUE;
}

unsigned int hz_update_crc32_fsc( unsigned int crc32, unsigned char c ) 
{
    unsigned int tmp, int_c;

    int_c = 0x000000ffL & (unsigned int) c;

    if ( ! crc_tab32_fsc_init ) init_crc32_fsc_table();

	tmp = (crc32 >> 24) ^ int_c;
    crc32 = (crc32 << 8) ^ crc_tab32_fsc[ tmp & 0xff ];

    return crc32;
}

/*
 * Width            = 32
 * Poly             = 0x04C11DB7L
 * InitValue(crc32) = 0xFFFFFFFFL
 */

unsigned int hz_calc_crc32_fsc( unsigned char *pSrc, unsigned int len, unsigned int crc32 ) 
{
	for(unsigned int i=0; i<len; i++) {
		crc32 = hz_update_crc32_fsc(crc32,pSrc[i]);
	}
	return crc32;
}

static PyObject * _crc32_fsc(PyObject *self, PyObject *args)
{
    const unsigned char* data;
    unsigned int data_len;
    unsigned int crc32 = 0xFFFFFFFFL;
    unsigned int result;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|I:fsc", &data, &data_len, &crc32))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|I:fsc", &data, &data_len, &crc32))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc32_fsc(data, data_len, crc32);

    return Py_BuildValue("I", result);
}


/*
*********************************************************************************************************
                                    POLY=0xEDB88320L [CRC32 for file]
*********************************************************************************************************
*/
void init_crc32_table( void ) 
{
    int i, j;
    unsigned int crc32;

    for (i=0; i<256; i++) {
        crc32 = (unsigned int) i;
        for (j=0; j<8; j++) {
            if ( crc32 & 0x00000001L )  crc32 = ( crc32 >> 1 ) ^ HZ32_POLYNOMIAL_CRC;
            else                        crc32 =   crc32 >> 1;
        }
        crc_tab32_crc[i] = crc32;
    }
    crc_tab32_crc_init = TRUE;
}

unsigned int hz_update_crc32( unsigned int crc32, unsigned char c ) 
{

    unsigned int tmp, int_c;

    int_c = 0x000000ffL & (unsigned int) c;

    if ( ! crc_tab32_crc_init ) init_crc32_table();

    tmp = crc32 ^ int_c;
    crc32 = (crc32 >> 8) ^ crc_tab32_crc[ tmp & 0xFF ];

    return crc32;
}

unsigned int hz_calc_crc32( unsigned char *pSrc, unsigned int len, unsigned int crc32 ) 
{
	for(unsigned int i=0; i<len; i++) {
		crc32 = hz_update_crc32(crc32, pSrc[i]);
	}
	crc32    ^= 0xFFFFFFFFL;
	return crc32;
}

static PyObject * _crc32_crc32(PyObject *self, PyObject *args)
{
    const unsigned char* data;
    unsigned int data_len;
    unsigned int crc32 = 0xFFFFFFFFL;
    unsigned int result;

#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "y#|I:crc32", &data, &data_len, &crc32))
        return NULL;
#else
    if (!PyArg_ParseTuple(args, "s#|I:crc32", &data, &data_len, &crc32))
        return NULL;
#endif /* PY_MAJOR_VERSION */

    result = hz_calc_crc32(data, data_len, crc32);

    return Py_BuildValue("I", result);
}


/* method table */
static PyMethodDef _crc32Methods[] = {
    {"fsc",     _crc32_fsc,    METH_VARARGS, "Calculate CRC (Ethernt's FSC) of CRC32 [Poly=0x04C11DB7, Init=0xFFFFFFFF]"},
    {"crc32",   _crc32_crc32,  METH_VARARGS, "Calculate CRC (File) of CRC32 [Poly=0xEDB88320L, Init=0xFFFFFFFF]"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


/* module documentation */
PyDoc_STRVAR(_crc32_doc,
"Calculation of CRC32 \n"
"libscrc.fsc -> Calculate CRC for Media file (MPEG) and Ethernet frame sequence (FSC) [Poly=0x04C11DB7, Init=0xFFFFFFFF]\n"
"libscrc.crc32 -> Calculate CRC for file [Poly=0xEDB88320L, Init=0xFFFFFFFF]\n"
"\n");


#if PY_MAJOR_VERSION >= 3

/* module definition structure */
static struct PyModuleDef _crc32module = {
   PyModuleDef_HEAD_INIT,
   "_crc32",                    /* name of module */
   _crc32_doc,                  /* module documentation, may be NULL */
   -1,                          /* size of per-interpreter state of the module */
   _crc32Methods
};

/* initialization function for Python 3 */
PyMODINIT_FUNC
PyInit__crc32(void)
{
    PyObject *m;

    m = PyModule_Create(&_crc32module);
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
init_crc32(void)
{
    (void) Py_InitModule3("_crc32", _crc32Methods, _crc32_doc);
}

#endif /* PY_MAJOR_VERSION */
