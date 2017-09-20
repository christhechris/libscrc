/*
*********************************************************************************************************
*                              		(c) Copyright 2006-2017, HZ, Studio
*                                           All Rights Reserved
* File    : _crc16tables.h
* Author  : Heyn (heyunhuan@gmail.com)
* Version : V0.1.0
* Web	  : http://heyunhuan513.blog.163.com
*
* LICENSING TERMS:
* ---------------
*		New Create at 	2017-09-19 21:01PM [Heyn] New CRC16-X25 Table.
*
*********************************************************************************************************
*/

#ifndef __CRC16_TABLES_H__
#define __CRC16_TABLES_H__

unsigned short hz_calc_crc16_r8408( const unsigned char *pSrc, unsigned int len, unsigned short crc16 );
unsigned short hz_calc_crc16_l1021( const unsigned char *pSrc, unsigned int len, unsigned short crc16 );

#endif //__CRC16_TABLES_H__
