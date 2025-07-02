#include <SPI.h>
#include <HardwareSerial.h>

#define TXDATAPORT       GPIOF       //PF13 in f746
#define TXDATAPIN        13
#define MODESELPORT0     GPIOE   //PF in f746
#define MODESELPORT1     GPIOF   //PF in f746
#define MODESELSW0	     13		 //Arduino A4 - STM Pf5 -sw 0 ; , PE13 for black module; ANT Rx
#define MODESELSW1     	 15       //Arduino A5 - STM PF10 - sw1  ; PF15 for black module; ANT Tx
#define TXMODE           0b01
#define RXMODE           0b10
#define MODEMASK         0b11
#define MODESELOFFSET	   0
#define TXAMPENPORT      GPIOE   //PA1 in f334, PC0 in f746, PE9 for black module
#define TXENPIN          9
#define RXPOWENPORT      GPIOD   //PD15  in f746
#define RXPOWENPIN       15
#define LNAENPORT        GPIOF   //PF12  in f746
#define LNAENPIN         12

#define RXDATAPORT		   GPIOF 			// PB5 in f334, PF14 in f746zg
#define RXDATAPIN		     14				

//#define SS PA6
#define SS PD14

HardwareSerial Serial2(PD6, PD5);  // (RX, TX)

void writeShiftRegister16(int ss_pin, uint16_t value) // Установка порога компаратора по SPI
{
  digitalWrite(ss_pin, LOW);
  /* Фокус вот в чём: сначала шлём старший байт */
  SPI.transfer(highByte(value));
  /* А потом младший */
  SPI.transfer(lowByte(value));
  digitalWrite(ss_pin, HIGH);
}

int gen = PF13; // PF13 (D7) пин – вход генератора 
int gen_amp = PE9; // PE9 (D6) пин – питание усилителя мощности 
int ant_rx = PE13; // PE13 (D3) пин – антенна на прием 
int ant_tx = PF15; // PF15 (D2) пин – антенна на передачу
int pow_rx = PD15; // PD15 (D9) пин – питание стабилизатора передатчика 
int lna = PF12; // PF12 (D8) пин – МШУ 
int comp_out = PF14; // PF14 (D4) пин – выход компаратора

// Значение порога компаратора
uint16_t nomad =  0b0000010001011101; //900 mV

void setup()
{
  SPI.begin();

  pinMode(gen, INPUT_PULLUP);
  pinMode(gen_amp, OUTPUT);
  pinMode(ant_rx, OUTPUT);
  pinMode(ant_tx, OUTPUT);
  pinMode(pow_rx, OUTPUT);
  pinMode(lna, OUTPUT);
  pinMode(comp_out, INPUT_PULLUP);
  
  pinMode(SS, OUTPUT);
  digitalWrite(SS, HIGH);
  writeShiftRegister16(SS, nomad);
  
  set_working_mode(RXMODE);  // Rx Mode

  Serial.begin(9600);
  Serial2.begin(2000000);
}

void set_working_mode(uint8_t mode)  // Установка рабочего режима (прием или передача)
{
  
	if(mode == TXMODE)
	{
    MODESELPORT0 ->ODR &= ~ (1 << MODESELSW0);  // ANT Rx Down
    MODESELPORT1 ->ODR |=   1 << MODESELSW1;    // ANT Tx Up
		//Rx Hardware: Rx Pow Down, LNA Down
		RXPOWENPORT->ODR &= ~ (1 << RXPOWENPIN);
		LNAENPORT  ->ODR &= ~ (1 << LNAENPIN);
        

		//Tx Hardware: Tx Amp Up, Tx Gen Up (inverse!!!)
		TXAMPENPORT->ODR |=    1 << TXENPIN;
    TXDATAPORT ->ODR |=   1 << TXDATAPIN;
	}
	else if(mode == RXMODE)
	{
    MODESELPORT1 ->ODR &= ~ (1 << MODESELSW1);  // ANT Tx Down 
    MODESELPORT0 ->ODR |=   1 << MODESELSW0;    // ANT Rx Up
		//Tx Hardware: Tx Amp Down, Tx Gen Up (inverse!!!)
		TXAMPENPORT	->ODR &= ~ (1 << TXENPIN);
    TXDATAPORT ->ODR |=   1 << TXDATAPIN;    

		//Rx Hardware: Rx Pow Up, LNA Up
		RXPOWENPORT->ODR  |=    1 << RXPOWENPIN;
		LNAENPORT  	->ODR |=    1 << LNAENPIN;

	}
}

uint8_t start_signal_COM4 = 140;

void loop() {

  set_working_mode(RXMODE);
  delay(1); 

  while(1){
    
    writeShiftRegister16(SS, nomad);
    delay(1);

    switch(Serial2.available() > 0){
      case true:
      {
        uint ff;
        ff = Serial2.read();
        
        if(ff == start_signal_COM4)
        {
          //Serial.write(ff);
          delay(1);
          set_working_mode(TXMODE);
          delay(1);
          
          for(int i = 0; i < 500000; i++){
            Serial2.write(224);
          }

          delay(10);
          set_working_mode(RXMODE);    
          delay(2);
        }

        break;
      }
      default: break;
    }
  }
  
}
