#include "functions.c"

int main(void) {
	DDRB = 0b11111111;	// All port B pins output.
	DDRC = 0b01000010;	// PC6 and PC1 output, rest input.
	DDRD = 0b11010000;	// PD7, PD6, and PD4 output, rest input.
	DDRF = 0b00010000;	// PF4 output, rest input.

	uart_init(BAUD_RATE);	// Init UART at 38400 baud
	CPU_PRESCALE(0x01);		// run at 8MHz.
	timer_init();			// Will set up PWM for heating, and hardware clock
	adc_init();				// Will set up ADC for reading the thermistor
	sei();					// Start interrupts.

	LED_OFF;

	while(1){	// see ATMEGA32U4 datasheet p.44
		// standby Mode Control Register default is off 0000 0000
		//SMCR = 00000110; // turn on power saving
		LED_ON;
		_delay_ms(500);						// Delay for a second
		LED_OFF;
		_delay_ms(500);						// Delay for a second
		uart_putchar('c');				// Send confirmation to RaspPi
		char x = uart_getchar();	// Receive reply from RaspPi

		// t 1 - Set temperature to 1
		// s 1 - Set stir speed to 1
		if(uart_getchar() == 't') {
			uart_putchar('h');
			run_temperature(1);
		} else if (uart_getchar() == 's') {
			uart_putchar('h');
			run_stir(1);
		}

		if(x == '?') {
			count_ms = 0;				// Reset hardware counter
			uart_putchar('h');	// Send confirmation to RaspPi
			uart_putchar('\n');	// Endline needed for RaspPi app's parsing
		}
	}
}

void run_temperature(char temp, int holdtime) {
	uint8_t ch = 0x00;								// Indicates PF0 as read port
	uint8_t tempin = (uint8_t)adc_read(ch)>>1; 		// Divide by 2

	uart_putchar('t');								// sends temperature data to RaspPi for realtime data monitoring
	uart_putchar(tempin);
	uart_putchar('\n');

	uint8_t temps = temp;							// Temperature currently for calculating deltas
	//changing to temp
	while(tempin < temp - 3 || tempin > temp + 3){	// While temperature is within 3mV of target
		uart_putstring("sc\n");						// Send changing flag to RaspPi
		hold = 0;									// find_duty() now knows we're not holding

		tempin = (uint8_t)adc_read(ch)>>1;			// Read temperature data for comparisons

		uart_putchar('t');							// Let RaspPi know the current temperature
		uart_putchar(tempin);
		uart_putchar('\n');

		find_duty(tempin, temp);
		else if(tempin < temps) {
			uart_putstring("dh\n");					// Send heating flag to RaspPi
			OCR1A = 0;
			OCR1B = duty;							// Set duty cycle to heating direction
		}
	}

	//holding temp, similar loop to above, but will hold a temperature for a set time
	count_ms = 0;
	while(count_ms < holdtime){
		uart_putstring("sh\n");				// Send hold flag to RaspPi
		hold = 1;							// find_duty() now knows that we're holding

		tempin = (uint8_t)adc_read(ch)>>1;			// Read temperature data for comparisons

		uart_putchar('t');					// Let RaspPi know the current temperature
		uart_putchar(tempin);
		uart_putchar('\n');

		find_duty(tempin, temps);
		if(tempin < temps){
			uart_putstring("dh\n");
			OCR1A = 0;
			OCR1B = duty;
			uint16_t x = count_ms;
			while(count_ms < x + 150){};
		} else {
			OCR1A = 0;
			OCR1B = 0;
		}
		hold = 0;							// find_duty() now knows that we're holding
	}

	uart_putstring("break\n");
	hold = 0;
}

void run_stir(char intensity) {

}

/* This function uses an equation to find the duty cycle that the PWM heating element
   should operate at at any given time. */
void find_duty(char tempin, char temp){
	/*if (hold == 0) {
	  if (temp < 72) { // 72 is 40C, describe more in depth
	  duty = 800+50*abs(temp-tempin);
	  }
	  else if (temp < 150 && temp > 72) {
	  duty = 200+200*abs(temp-tempin);
	  }
	  else if (temp < 224 && temp > 150) {
	  duty = 200+300*abs(temp-tempin);
	  }

	  if (duty > 1023) {
	  duty = 1023;
	  }
	  }
	  if (hold == 1) {
	  if (temp > 60 && temp < 80) {
	  duty = 400;	// hardcode these values as global definitions
	  }
	  if (temp > 130 && temp < 170) {
	  duty = 400;
	  }
	  if (temp > 214 && temp < 230) {
	  duty = 600;
	  }
	  }*/
	duty = 1023;
}
