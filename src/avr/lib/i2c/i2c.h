#ifndef i2c_header
#define i2c_header

#define F_CPU 8000000
#include <avr/io.h>
#include <avr/pgmspace.h>
#include <util/delay.h>
#include <stdint.h>

	void ERROR();
	void initI2C();
	void batteryICI2C(uint8_t, uint8_t);
	uint8_t I2C_receive_batteryIC(uint8_t);

#endif
