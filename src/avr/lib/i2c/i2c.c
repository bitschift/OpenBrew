#include "i2c.h"


#define START 0x08
#define ReSTART 0x10
#define SLAWACK 0x18
#define SLAWnoACK 0x20

//TWI bus lines: PD0 SCL, PD1 SDA.
//IC add is 0x6A
//charges at .5 amps, limited to 1 amp


// TWDR shift register contains address and data
// TWCR contains acknowledgment bit manipulation in recieve mode
// TWSR contains acknowledgment bit value check
void ERROR1()
{
  while(1);

}

void ERROR2()
{	
  return;
}


void initI2C()
{
  DDRD = 0;
  PORTD = ((1<<DDD0) | (1<<DDD1));     //PD0 and PD1
  TWBR = 11;  //sets bitrate
}

void batteryICI2C(uint8_t DATA1, uint8_t DATA2)
{

  TWCR = (1<<TWINT) | (1<<TWSTA) | (1<<TWEN); //Send Start condition

  while (!(TWCR & (1<<TWINT)))    //breaks when TWINT == 1
    ;			//Wait for transmission to complete

  if ((TWSR & 0xF8) != START)
    ERROR2();               //If START condition not received, error


  TWDR = 0xD4;
  TWCR = (1<<TWINT) | (1<<TWEN);  //Load SLA+W then initiate transfer

  while (!(TWCR & (1<<TWINT)))
    ;			//Wait for transmission to complete


  if ((TWSR & 0xF8) != 0x18)
    ERROR2();		//ERROR if SLA+W not sent and acknowledged


  TWDR = DATA1;
  TWCR = (1<<TWINT) | (1<<TWEN);  //Load SDA, start transmission

  while (!(TWCR & (1<<TWINT)))
    ;			//Wait for transmission to complete

  if((TWSR & 0xF8) != 0x28)	//ERROR if SDA
    ERROR2();

  TWDR = DATA2;
  TWCR = (1<<TWINT) | (1<<TWEN);  //Load SDA, start transmission

  while (!(TWCR & (1<<TWINT)))
    ;

  if((TWSR & 0xF8) != 0x28)
    ERROR2();

  TWCR = (1<<TWINT) | (1<<TWEN) | (1<<TWSTO); //send stop condition

}	


uint8_t I2C_receive_batteryIC(uint8_t data2)  //parameters: register address    returns: register
{

  uint8_t data1 = 0; 


  TWCR = (1<<TWINT) | (1<<TWSTA) | (1<<TWEN); //Send Start condition

  while (!(TWCR & (1<<TWINT)))    //breaks when TWINT == 1
    ;			//Wait for transmission to complete

  if ((TWSR & 0xF8) != START)
    ERROR2();               //If START condition not received, error


  TWDR = 0xD4;
  TWCR = (1<<TWINT) | (1<<TWEN);  //Load SLA+W then initiate transfer

  while (!(TWCR & (1<<TWINT)))
    ;			//Wait for transmission to complete


  if ((TWSR & 0xF8) != 0x18)
    ERROR2();		//ERROR if SLA+W not sent and acknowledged


  TWDR = data2;
  TWCR = (1<<TWINT) | (1<<TWEN);  //Load data, start transmission

  while (!(TWCR & (1<<TWINT)))
    ;			//Wait for transmission to complete

  if((TWSR & 0xF8) != 0x28)	
    ERROR2();






  TWCR = (1<<TWINT) | (1<<TWSTA) | (1<<TWEN);    //repeat start condition

  while (!(TWCR & (1<<TWINT)))    //breaks when TWINT == 1
    ;			//Wait for transmission to complete

  if((TWSR & 0xF8) != 0x10)  //Error for repeat start condition
    ERROR2();


  TWDR = 0xD5;   //SLA+R

  TWCR = (1<<TWINT) | (1<<TWEN);  //load data


  while (!(TWCR & (1<<TWINT)))
    ;			//Wait for transmission to complete


  if((TWSR & 0xF8) != 0x40)  // checks if SLA+R and ACK has been sent
    ERROR2();



  TWCR = (1<<TWINT) | (1<<TWEN) | (1<<TWEA);  //ready to receive,  ACK

  while (!(TWCR & (1<<TWINT)))  // wait for reception
    ;

  data1 = TWDR;

  TWCR = (1<<TWINT) | (1<<TWEN);   //send no ACK

  while (!(TWCR & (1<<TWINT)))  // wait for reception
    ;

  TWCR = (1<<TWINT) | (1<<TWEN) | (1<<TWSTO); //send stop condition

  return data1; 

}


