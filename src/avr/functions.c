#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <avr/eeprom.h>
#include <avr/pgmspace.h>
#include <stdio.h>
#include "main.h"

// Bluetooth/USART Transmit Interrupt
ISR(USART1_UDRE_vect) {
	uint8_t i;

	if (tx_buffer_head == tx_buffer_tail) {
		// buffer is empty, disable transmit interrupt, enable RX complete interrupt
		UCSR1B = (1<<RXEN1) | (1<<TXEN1) | (1<<RXCIE1);
	} else {
		i = tx_buffer_tail + 1;
		if (i >= TX_BUFFER_SIZE) i = 0;
		UDR1 = tx_buffer[i]; // write data to TX
		tx_buffer_tail = i;
	}
}

// Bluetooth/USART Receive Interrupt
ISR(USART1_RX_vect) {
	uint8_t c, i;

	c = UDR1; // read data from RX
	i = rx_buffer_head + 1;
	if (i >= RX_BUFFER_SIZE) i = 0;
	if (i != rx_buffer_tail) {
		rx_buffer[i] = c;
		rx_buffer_head = i;
	}
}

// This interrupt triggers every millisecond and
// increments a timer that is reset periodically with in the main functional code.
ISR(TIMER3_COMPA_vect) {
	count_ms++;
}

// This interrupt is for when an interrupt goes wrong.
ISR(BADISR_vect) {
	PORTD = 0xFF;
	uart_putstring("Bad\n");
	while(1){};
}

void adc_init(void) {
	//AREF = AVcc
	DIDR0 = (1 << ADC4D) | (1<<ADC1D) | (1<<ADC0D); //Reduce the power for the pins used as ADC pins
	ADMUX = (1 << REFS0); //Set ADC Reference to default of Vcc
	//adc enable and prescaler of 128
	ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); //Enable the ADC and Set prescalar to 128
}

int16_t adc_read(uint8_t mux) {
	uint8_t low;

	ADCSRA = (1<<ADEN) | ADC_PRESCALER;             // enable ADC
	ADCSRB = (1<<ADHSM) | (mux & 0x20);             // high speed mode
	ADMUX = aref | (mux & 0x1F);                    // configure mux input
	ADCSRA = (1<<ADEN) | ADC_PRESCALER | (1<<ADSC); // start the conversion
	while (ADCSRA & (1<<ADSC)) ;                    // wait for result
	low = ADCL;                                     // must read LSB first
	return (ADCH << 8) | low;                       // must read MSB only once!
}

void uart_init(uint32_t baud) {
	UBRR1 = (F_CPU / 4 / baud - 1) / 2;				// This register sets the baud rate to 38400
	UCSR1A = (1<<U2X1);								// Double transfer rate.
	UCSR1B = (1<<RXEN1) | (1<<TXEN1) | (1<<RXCIE1);	// Enable USART Receiver, enable transmitter, and enable RX interrupt
	UCSR1C = (1<<UCSZ11) | (1<<UCSZ10);				// Set 8-bit character size.
	tx_buffer_head = tx_buffer_tail = 0;
	rx_buffer_head = rx_buffer_tail = 0;
}

uint8_t rx_bytes_available(void) {
	uint8_t head, tail;

	head = rx_buffer_head;
	tail = rx_buffer_tail;
	if (head >= tail) return head - tail;
	return RX_BUFFER_SIZE + head - tail;
}

uint8_t rx_getchar(void) {
    uint8_t c, i;

	while (rx_buffer_head == rx_buffer_tail) ; // wait for character
    i = rx_buffer_tail + 1;
    if (i >= RX_BUFFER_SIZE) i = 0;
    c = rx_buffer[i];
    rx_buffer_tail = i;
    return c;
}

void tx_putchar(char c) {
	uint8_t i;

	i = tx_buffer_head + 1;
	if (i >= TX_BUFFER_SIZE) i = 0;
	while (tx_buffer_tail == i) ; // wait until space in buffer
	tx_buffer[i] = c;
	tx_buffer_head = i;
	// enable data register empty and RX complete interrupt, verify RX and TX are enabled
	UCSR1B = (1<<RXEN1) | (1<<TXEN1) | (1<<RXCIE1) | (1<<UDRIE1);
}

void tx_putstring(char *s) {
	int i = 0;
	while(s[i] != '\0'){
		uart_putchar(s[i]); // Runs a loop to paste all characters in an array.
		i++;
	}
}

void timer_init(void) {
	// Timer 3
	TCCR3A = 0b00000000;	// Setting TCCR3A Mode to CTC. Since bit 0 (WGM10), and
							// bit1 (WGM11) are set to zero for both CTC setting we
							// can set TCCR0A = 0000 0000

	TCCR3B = 0b00001010;	// Setting TCCR1B initial value to 256 prescaler & setting CTC
							// output mode (ATMEGA32U4 datasheet p.133, p.331 respectively). TCCR1B = 0000 1010

	TIMSK3 = 0b00000010;	// The OCIE1A bit enables interrupt flag.

	OCR3A = 1000;			// timer compare value   8MHz/8 = 1MHZ = 1 second (out of range), and 1000 = 1ms
	TCNT3 = 0;				// Initiates the timer to count CPU cycles.

	// Timer 1
	TCCR1A = 0b11110011;	// OC1A/OC1B on compare match, clear OC1A/OC1B at TOP, 10-bit fast PWM
	TCCR1B = 0b00001101;	// 10-bit fast PWM, clk/64 PWM clock
}