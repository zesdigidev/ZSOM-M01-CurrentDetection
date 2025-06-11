#ifndef Fram_Ctrl_h
#define Fram_Ctrl_h
//**************************************************************************************************
//
//  Do NOT modify or remove this copyright and confidentiality notice!
//  Copyright (C) ZERO-ERROR SYSTEMS 2023 All rights reserved
//
//  This module is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
//
//**************************************************************************************************

#define KBYTE               1024
#define NUM_BITS_IN_BYTE    8
#define FRAM_CS     5

//*************************************************************
// SPISettings
//*************************************************************
#define SPI_MAX_SPEED   33000000     // 33 MHz SCK (max)
//#define SPI_MAX_SPEED   4000000     // 4 MHz SCK
#define SPI_DATA_ORDER  MSBFIRST    // MSBFIRST or LSBFIRST
#define SPI_DATA_MODE   SPI_MODE0   // SPI_MODE0 or SPI_MODE1 or SPI_MODE2 or SPI_MODE3


//*************************************************************
// FRAM address map
//*************************************************************
#define FRAM_SIZE                         (32 * KBYTE)

#define FRAM_BASE_ADDRESS                 ( 0 )
#define FRAM_DATA_SIZE                    ( 1 * KBYTE )


//*************************************************************
// FRAM OP-CODE
//*************************************************************
#define FRAM_WREN  0x06 // 0000 0110b // Set Write Enable Latch
#define FRAM_WRDI  0x04 // 0000 0100b // Reset Write Enable Latch
#define FRAM_RDSR  0x05 // 0000 0101b // Read Status Register
#define FRAM_WRSR  0x01 // 0000 0001b // Write Status Register
#define FRAM_READ  0x03 // 0000 0011b // Read Memory Code
#define FRAM_WRITE 0x02 // 0000 0010b // Write Memory Code
#define FRAM_RDID  0x9F // 1001 1111b // Read Device ID
#define FRAM_SLEEP 0x06 // 1011 1001b // Sleep Mode


//*************************************************************
// Variable
//*************************************************************
// FRAM
int iFramArray[KBYTE/sizeof(int)] = {0};    // 256 * 4byte = 1024bytes = 1KB
int iFramRdArray[KBYTE/sizeof(int)] = {0};


//*************************************************************
// Function declaration
//*************************************************************




#endif //#ifndef Fram_Ctrl_h
