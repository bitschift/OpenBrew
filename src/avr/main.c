#include "functions.c"

int main(void) {
	DDRB = 0b11111111;	// All port B pins output.
	DDRC = 0b01000010;	// PC6 and PC1 output, rest input.
	DDRD = 0b11010000;	// PD7, PD6, and PD4 output, rest input.
	DDRF = 0b00010000;	// PF4 output, rest input.

	uart_init(BAUD_RATE);	// Init UART at 38400 baud
	CPU_PRESCALE(0x01);		// run at 8MHz.
	timer_init();			// Will set up PWM for Peltier and hardware clock
	adc_init();				// Will set up ADC for reading the thermistor
	sei();					// Start interrupts.

	LED_OFF;

    while(1){	// If not command is sent the PCR will enter power saving "idle mode" see ATMEGA32U4 datasheet p.44
        // standby Mode Control Register default is off 0000 0000
        //SMCR = 00000110; // turn on power saving
        LED_ON;
    	_delay_ms(500);			// Delay for a second
    	LED_OFF;
        _delay_ms(500);			// Delay for a second
    	uart_putchar('c');			// Send confirmation to Android
    	char x = uart_getchar();	// Receive reply from Android
        if(x == '?') {
            count_ms = 0;			// Reset hardware counter
            uart_putchar('h');		// Send confirmation to Android
            uart_putchar('\n');		// Endline needed for Android app's parsing
            pcr_init();				// Receive user settings from Android
            run_pcr();				// Run PCR using user settings for time and temperature
        }
	}
}

void phase(char temp, char time){
    uint16_t timer = time * 1000;					// Converts user-provided seconds to milliseconds
	uint8_t ch = 0x00;								// Indicates PF0 as read port
	uint8_t tempin = (uint8_t)adc_read(ch)>>1; 		// Divide by 2

	uart_putchar('t');								// sends temperature data to Android for realtime data monitoring
	uart_putchar(tempin);
	uart_putchar('\n');

	uint8_t temps = temp;							// Temperature currently for calculating deltas
	//changing to temp
	while(tempin < temp - 3 || tempin > temp + 3){	// While temperature is within 3mV of target
		uart_putstring("sc\n");						// Send changing flag to Android
		hold = 0;									// find_duty() now knows we're not holding

		tempin = (uint8_t)adc_read(ch)>>1;			// Read temperature data for comparisons

		uart_putchar('t');							// Let Android know the current temperature
		uart_putchar(tempin);
		uart_putchar('\n');

		find_duty(tempin, temp);
		if(tempin > temps) {
			uart_putstring("dc\n");					// Send cooling flag to Android
			OCR1A = duty;							// Set duty cycle to heating direction
			OCR1B = 0;
		}
		else if(tempin < temps) {
			uart_putstring("dh\n");					// Send heating flag to Android
			OCR1A = 0;
			OCR1B = duty;							// Set duty cycle to cooling direction
		}
	}

	//holding temp, similar loop to above, but will hold a temperature for a set time
	count_ms = 0;
	while(count_ms < timer){
		uart_putstring("sh\n");				// Send hold flag to Android
		hold = 1;							// find_duty() now knows that we're holding

		tempin = (uint8_t)adc_read(ch)>>1;			// Read temperature data for comparisons

		uart_putchar('t');					// Let Android know the current temperature
		uart_putchar(tempin);
		uart_putchar('\n');

		find_duty(tempin, temps);
		if(tempin > temps){
			uart_putstring("dc\n");
			OCR1A = duty;
			OCR1B = 0;
			uint16_t x = count_ms;
			while(count_ms < x + 150){};
		}
		else if(tempin < temps){
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

void pcr_init(void){
	char pcr_set[15];
	pcr_set[0] = '0';
    pcr_set[13] = '\n';
	pcr_set[14] = '\0';
	// while loop will check with user to verify that input are correct.
	while(1){
		//Getting user settings from bluetooth (12 values: 6 temp, 6 time)
		uint8_t i;
		for(i=1; i<13;i++){
			pcr_set[i]= uart_getchar();
		}

		//Confirming user settings
		uart_putchar(1);
        uart_putstring(pcr_set);
		
		if(uart_getchar() != '0'){
    		//********** PCR Steps Time & Temperature

			// Initialization step:
			init_step_time = pcr_set[1];
			init_step_temp = pcr_set[2];

			//Denaturation step:
			Den_step_time = pcr_set[3];
			Den_step_temp = pcr_set[4];

			// Annealing step:
			ann_step_time = pcr_set[5];
			ann_step_temp = pcr_set[6];

			//Extension/elongation step:
			ext_step_time = pcr_set[7];
			ext_step_temp = pcr_set[8];

			//Final elongation step:
			f_elon_step_time = pcr_set[9];
			f_elon_step_temp = pcr_set[10];

			//Final hold:
			f_hold_step_time = pcr_set[11];
			f_hold_step_temp = pcr_set[12];

            uart_putstring("START!\n");
            
            break;
		}
	}
}

void run_pcr (void){
	char x;
	for(x = 0; x < 30; x ++){
		uart_putchar('y'); // send Android current cycle
		uart_putchar(x+1);
		uart_putchar('\n');

		uart_putstring("p1\n"); // send Android current phase
		phase(Den_step_temp, Den_step_time); // initiate denaturing
		uart_putstring("p2\n");
		phase(ann_step_temp, ann_step_time); // initiate annealing
		uart_putstring("p3\n");
		phase(ext_step_temp, ext_step_time); // initiate extension
	}
}

/* This function uses an equation to find the duty cycle that the PWM-powered Peltier junction
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