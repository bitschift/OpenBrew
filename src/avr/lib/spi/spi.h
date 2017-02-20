#ifndef spi_header
#define spi_header

#define F_CPU 8000000
#include <avr/io.h>
#include <avr/pgmspace.h>
#include <util/delay.h>
#include <stdint.h>

	void SPI_masterInit(void);
	int8_t SPI_masterTransmit(int8_t cData);
	int8_t SPI_masterReceive(void);
#endif
