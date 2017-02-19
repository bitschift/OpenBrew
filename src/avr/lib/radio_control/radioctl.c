#include "../radio_control/radioctl.h"
#include "../spi/spi.h"

/*************** PORT OPERATIONS ****************/

void openPort()
{
  CSN_LOW;
}

void closePort()
{ 
  CSN_HIGH;        // sets port high
  while(!(CSN_PIN_R &= (1<<CSN_PIN)))    //while port is low
    ;
}

/*************** Radio Functions ******************/

void initRadioTX()
{
  openPort();
  SPI_masterTransmit(0b00100000);
  SPI_masterTransmit(0b00001010);  // sets TX mode on 
  closePort();
}

void initRadioRX()
{
  openPort(); 
  SPI_masterTransmit(0b00100000);
  SPI_masterTransmit(0b00001011);  // sets RX mode on 
  closePort();
}

/***********************************************************
  This function activates the following features
  -R_RX_PL_WID
  -W_ACK_PAYLOAD
  -W_TX_PAYLOAD_NOACK
  If not used, writing to these registers has no effect
 *************************************************************/

void activateFeatures()
{
  openPort();
  SPI_masterTransmit(0b01010000);
  SPI_masterTransmit(0x73);
  closePort();
}

/*************************************************************/

void setRadioAddressWidth(uint8_t width)
{
  openPort();
  SPI_masterTransmit(0b00100011);  // setup_aw register
  SPI_masterTransmit(width);  // sets address 
  closePort();
}

void setRadioFrequency(uint8_t frequency)
{
  openPort();
  SPI_masterTransmit(0b00100101);  // addresses radio frequency register 
  SPI_masterTransmit(frequency);  // sets frequency 
  closePort(); 
}

void setRadioTXAddress(uint32_t address)
{
  uint8_t addLow = address;
  uint8_t addMid = (address >> 8);
  uint8_t addHigh = (addMid >> 8);

  openPort();
  SPI_masterTransmit(0x30);  // TX_ADDR register
  SPI_masterTransmit(addLow);  // receive address for data pipe 0
  SPI_masterTransmit(addMid); 
  SPI_masterTransmit(addHigh); 

  closePort();
}

void setRadioRXAddress(int32_t address)
{
  uint8_t addLow = address;
  uint8_t addMid = (address >> 8);
  uint8_t addHigh = (addMid >> 8);

  openPort();
  SPI_masterTransmit(0x2A);  // RX_ADDR_P0 register
  SPI_masterTransmit(addLow);  // receive address for data pipe 0
  SPI_masterTransmit(addMid); 
  SPI_masterTransmit(addHigh); 

  closePort();
}


/***********************************************************
  size is the number of bytes in PL from 1-32
 ************************************************************/


void setRadioRXPayloadSize(uint8_t dataPipe, uint8_t size)
{
  openPort();
  SPI_masterTransmit(dataPipe | 0b00100000);  //address data pipe
  SPI_masterTransmit(size);  // size of payload for data pipe
  closePort();
}

void setRadioTXPayload(uint8_t* frame, int8_t payloadSize)
{
  openPort();
  SPI_masterTransmit(0b10100000);  // Initiate writing of payload
  for(int i = 0; i < payloadSize; i++)
  {
    SPI_masterTransmit(frame[i]);
  }
  closePort();
}


void getRadioRXPayload(uint8_t* payload, uint8_t payloadSize)
{
  uint8_t radioStatus;
  openPort();
  radioStatus = SPI_masterTransmit(0b01100001); //read payload 8 bytes
  for(int i = 0; i<payloadSize; i++)
  {
    payload[i] = SPI_masterReceive();
  }
  closePort();
}


void getRadioStatus(uint8_t* status)
{
  openPort();
  *status = SPI_masterTransmit(0x07);  // RX_ADDR_P0 register, radioStatus now == status
  closePort();
}






/**************************************************
  Boolean valued functions. return 1 if bit
  is set, else returns 0 
 ***************************************************/




uint8_t getRX_DR()
{
  uint8_t status;
  getRadioStatus(&status);
  if(status & (1<<6))  // if RX_DR is set
    return 1;
  else
    return 0;
}

uint8_t getTX_DS()
{
  uint8_t status;
  getRadioStatus(&status);
  if(status & (1<<5))  
    return 1;
  else
    return 0;
}

uint8_t getMAX_RT()
{
  uint8_t status;
  getRadioStatus(&status);
  if(status & (1<<4))  
    return 1;
  else
    return 0;
}

uint8_t getTX_FULL()
{
  uint8_t status;
  getRadioStatus(&status);
  if(status & (1<<0))  
    return 1;
  else
    return 0;
}




/*********** Clear Status Bits **************/




void clearMAX_RT()
{   
  uint8_t status;
  openPort();
  status = SPI_masterTransmit(0x07 | 0b00100000);  
  SPI_masterTransmit(status |= (1<<4));
  closePort();
}

void clearTX_DS()
{
  uint8_t status;
  openPort();
  status = SPI_masterTransmit(0x07 | 0b00100000);  
  SPI_masterTransmit(status |= (1<<5));
  closePort();
}

void clearRX_DR()
{
  uint8_t status;
  openPort();
  status = SPI_masterTransmit(0x07 | 0b00100000); 
  SPI_masterTransmit(status |= (1<<6));  //reset receive bit
  closePort();
}



