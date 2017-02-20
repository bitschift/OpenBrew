#include"spi.h"

void SPI_masterInit()
{
	/* Set MOSI, /SS and SCK to output, all others to input */
	DDRB = ((1<<DDB0) | (1<<DDB2) | (1<<DDB1));

	/* Enable SPI and Master mode, set clock rate to fck/4 */
	SPCR = (1<<SPE) | (1<<MSTR);
}


int8_t SPI_masterReceive(void)
{
	SPDR = 0xFF; 			// Dummy variable
	while(!(SPSR & (1<<SPIF))){}
	return SPDR;
}

int8_t SPI_masterTransmit(int8_t cData)
{
	SPDR = cData;
	while(!(SPSR & (1<<SPIF))){}
	return SPDR;
}
