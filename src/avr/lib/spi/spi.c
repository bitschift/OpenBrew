#include"spi.h"



/************* Basic SPI Functions ****************/




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







/*********** Music Collab Functions ***************/




void digiPotInitWiper(uint8_t cData)
{
	//  DDRD = (1<<DDD6);  //sets PD6 as output port
	PORTD = PORTD & ~(0x40); //sets PD6 output low
	SPI_masterTransmit(0x00);
	SPI_masterTransmit(cData);
	//  _delay_ms(100);
	PORTD = PORTD | (0x40); //sets PD output high
	//  _delay_ms(100);
}

void accelerometerReceive(int8_t *acc)
{
	int8_t temp;
	//int8_t *acc = (int8_t*)malloc(6*sizeof(int8_t));
	PORTD = PORTD & ~(0x80); //sets PD7 output low
	SPI_masterTransmit(0b11110010);//recieve XL
	acc[1] = SPI_masterTransmit(0x72);
	acc[0] = SPI_masterTransmit(0x72);// XH
	acc[3] = SPI_masterTransmit(0x72);// YL
	acc[2] = SPI_masterTransmit(0x72);// YH
	acc[5] = SPI_masterTransmit(0x72);// ZL
	acc[4] = SPI_masterTransmit(0x72);// ZH
	PORTD = PORTD | (0x80);
	//return acc;
	
}

void init_accel(void)
{
	//Changes clock polarity and clock phase for accelerometer
	SPCR |= ((1<<CPOL) | (1<<CPHA));
	PORTD = PORTD & ~(0x80);
	SPI_masterTransmit(0b00101101);  //access writing to power register
	SPI_masterTransmit(0x08);  //places accelerometer in measurement mode
	PORTD = PORTD | (0x80);
}




