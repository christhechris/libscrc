/*
*********************************************************************************************************
*                              		(c) Copyright 2006-2017, HZ, Studio
*                                           All Rights Reserved
* File    : _crc16tables.c
* Author  : Heyn (heyunhuan@gmail.com)
* Version : V0.1.0
* Web	  : http://heyunhuan513.blog.163.com
*
* LICENSING TERMS:
* ---------------
*		New Create at 	2017-09-20 21:57PM [Heyn]
*
*********************************************************************************************************
*/

#include "_crc16tables.h"

#define                 TRUE                                    1
#define                 FALSE                                   0

#define                 MAX_TABLE_ARRAY                         256

#define                 CRC16_POLYNOMIAL_R8408                  0x8408
#define                 CRC16_POLYNOMIAL_L1021                  0x1021

static unsigned short   crc16_tab_shift_r8408[MAX_TABLE_ARRAY]  = {0x0000};    // Used for X25 Kermit
static unsigned short   crc16_tab_shift_l1021[MAX_TABLE_ARRAY]  = {0x0000};    // Used for CCITT-FALSE XModem

static int              crc16_tab_shift_r8408_init              = FALSE;
static int              crc16_tab_shift_l1021_init              = FALSE;

/*
*********************************************************************************************************
                                    POLY=0x8408 [X25\Kermit]
*********************************************************************************************************
*/

static void _init_crc16_table_r8408( void ) 
{
    unsigned int i = 0, j = 0;
    unsigned short crc, c;

    for ( i=0; i<MAX_TABLE_ARRAY; i++ ) {
        crc = 0;
        c   = (unsigned short) i;
        for ( j=0; j<8; j++ ) {
            if ( (crc ^ c) & 0x0001 ) crc = ( crc >> 1 ) ^ CRC16_POLYNOMIAL_R8408;
            else                      crc =   crc >> 1;
            c = c >> 1;
        }
        crc16_tab_shift_r8408[i] = crc;
    }
    crc16_tab_shift_r8408_init = TRUE;
}

static unsigned short _hz_update_crc16_r8408( unsigned short crc16, unsigned char c ) 
{
    unsigned short crc = crc16;
    unsigned short tmp, short_c;

    short_c = 0x00FF & (unsigned short) c;
    if ( ! crc16_tab_shift_r8408_init ) _init_crc16_table_r8408();

    tmp =  crc       ^ short_c;
    crc = (crc >> 8) ^ crc16_tab_shift_r8408[ tmp & 0xFF ];

    return crc;
}

unsigned short hz_calc_crc16_r8408( const unsigned char *pSrc, unsigned int len, unsigned short crc16 )
{
    unsigned int i = 0;
    unsigned short crc = crc16;

	for ( i=0; i<len; i++ ) {
		crc	= _hz_update_crc16_r8408(crc, pSrc[i]);
	}
	return crc;
}

/*
*********************************************************************************************************
                                    POLY=0x1021 [CCITT-FALSE\XModem]
*********************************************************************************************************
*/

static void _init_crc16_table_l1021( void ) 
{
    unsigned int i = 0, j = 0;
    unsigned short crc, c;

    for ( i=0; i<256; i++ ) {
        crc = 0;
        c   = ((unsigned short) i) << 8;
        for ( j=0; j<8; j++ ) {
            if ( (crc ^ c) & 0x8000 ) crc = ( crc << 1 ) ^ CRC16_POLYNOMIAL_L1021;
            else                      crc =   crc << 1;
            c = c << 1;
        }
        crc16_tab_shift_l1021[i] = crc;
    }
    crc16_tab_shift_l1021_init = TRUE;
}

static unsigned short _hz_update_crc16_l1021( unsigned short crc16, unsigned char c )
{
    unsigned short crc = crc16;
    unsigned short tmp, short_c;

    short_c  = 0x00FF & (unsigned short) c;

    if ( ! crc16_tab_shift_l1021_init ) _init_crc16_table_l1021();

    tmp = (crc >> 8) ^ short_c;
    crc = (crc << 8) ^ crc16_tab_shift_l1021[tmp];

    return crc;
}

unsigned short hz_calc_crc16_l1021( const unsigned char *pSrc, unsigned int len, unsigned short crc16 )
{
    unsigned int i = 0;
    unsigned short crc = crc16;

	for ( i=0; i<len; i++ ) {
		crc = _hz_update_crc16_l1021(crc, pSrc[i]);
	}
	return crc;
}