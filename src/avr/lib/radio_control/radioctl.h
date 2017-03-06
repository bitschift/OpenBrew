#ifndef radioctl_h_
#define radioctl_h_

#include <avr/io.h>
#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <avr/cpufunc.h>
#include <stdlib.h>


#define THREE_BYTES 0b00000001
#define FOUR_BYTES 0b00000010
#define FIVE_BYTES 0b00000011 

#define DATA_PIPE_0 0x11 

/*************************************************************************
	Use this to define which pin on the MCU the select bit is connected to.
	first determine the port, followed by the pin. The port should be 
	defined in all caps (ex. PORTF), and no extra spaces. The PIN should
	simply be an integer value between 0 and 7. The PIN macro should
	be set to the PIN register of the port being used, ex. if CSN_PORT
	= PORTF, then PIN = PINF. Lastly, the CSN_DDR should be set to the
	data direction register of the port being used.                            
 ************************************************************************/

#define CSN_PORT PORTF
#define CSN_PIN 4
#define CSN_PIN_R PINF
#define CSN_DDR DDRF

/*************************************************************************
	Similarly, use this to define which port line CE on the radio is 
	connected to as well as the PIN number and DDR register
*************************************************************************/

#define CE_PORT PORTF
#define CE_PIN 1
#define CE_DDR DDRF

/*************************************************************************/

#define INIT_CSN (CSN_DDR |= (1<<CSN_PIN))
#define INIT_CE (CE_DDR |= (1<<CE_PIN))

#define CE_LOW (CE_PORT &= ~(1<<CE_PIN))
#define CE_HIGH  (CE_PORT |= (1<<CE_PIN))

#define CSN_LOW (CSN_PORT &= ~(1<<CSN_PIN))
#define CSN_HIGH (CSN_PORT |= (1<<CSN_PIN))


void initRadioTX(void);
void initRadioRX(void);

void activateFeatures(void);

void setRadioAddressWidth(uint8_t width);
void setRadioFrequency(uint8_t frequency); 
void setRadioTXAddress(uint32_t address);
void setRadioRXAddress(int32_t address);
void setRadioTXPayload(uint8_t* frame, int8_t payloadSize);
void setRadioRXPayloadSize(uint8_t dataPipe, uint8_t size);

void getRadioRXPayload(uint8_t* payload, uint8_t payloadSize);
void getRadioStatus(uint8_t* status);


uint8_t getRX_DR();
uint8_t getTX_DS();
uint8_t getMAX_RT();
uint8_t getTX_FULL();


void clearMAX_RT();
void clearTX_DS();
void clearRX_DR();


#endif









