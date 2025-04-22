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
  Serial.begin(2000000);
  Serial2.setTimeout(1000);
  Serial2.begin(3000000);
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

uint16_t sum_1;
uint16_t max_threshold; 
uint16_t min_threshold; 
uint16_t threshold;
uint16_t old_threshold;
uint16_t MAX_SUM = 2047; //135; //135; //135; //405; //405; //335; //3375; //335; //3375; //338; // //9000
uint16_t LOW_BOUND = 0.4*MAX_SUM; //0.4*MAX_SUM; //0.2*MAX_SUM; //MAX_SUM/4; //0.05*MAX_SUM; //1000;
uint32_t sum_threshold = 0;
float mean_threshold = 0;
unsigned int NUM_TH = 1;
unsigned int ii = 0; 
unsigned int mm = 0;
int bb = 0;
uint16_t req_len;

uint8_t start_signal_COM5 = 120;
uint8_t start_signal_COM6 = 140;
uint8_t listen_signal = 100; 

void loop() {

  set_working_mode(RXMODE);

  while(1){ 

    delay(1); 
    writeShiftRegister16(SS, nomad);
    delayMicroseconds(100);
  
    switch (Serial.available() > 0) {
      case true:
      {
        int data = Serial.parseInt();

        if (data == start_signal_COM5 || data == start_signal_COM6){
          Serial.write(data);
          set_working_mode(TXMODE);
          delay(5);
          
          Serial2.write(data);  

          delay(2);
          set_working_mode(RXMODE);
          delay(2);

          Serial.flush();
        }
        
        if (data = listen_signal){
          req_len = data;

          Serial.print(req_len); // Подтверждает получение запроса, отправляя полученное значение длины пакета
          Serial.print('\n');
          //delayMicroseconds(500); // Вот это я не помню. Нужна ли там задержка... 
        
          float buf[req_len] = {0}; //  Массив для результатов измерений
          
          for (int bb = 0; bb < req_len; bb++) {  // Цикл измерений
              
            mean_threshold = 0;
            for (mm = NUM_TH; mm > 0; mm--){ // Может усреднять несколько измерений если NUM_TH>1
              max_threshold = 0b0000101000101110; //2100 mV  // Максимальный порог
              min_threshold = nomad; // Минимальный порог
              old_threshold = 0;
              threshold = nomad;  // Текущее значение порога
              
              while (threshold != old_threshold) {
                writeShiftRegister16(SS, threshold); // Выставляем порог на компараторе
                sum_1 = 0;
                for (ii = MAX_SUM; ii > 0; ii--){  // Считываем MAX_SUM значений из регистра выхода компаратора     
                  sum_1 += ((RXDATAPORT->IDR & (1 << RXDATAPIN)) == 0);
                }   
                if ((LOW_BOUND <= sum_1)) {  // Если единиц больше чем LOW_BOUND (в данном случае больше чем четверть отсчетов) - повышаем порог
                  min_threshold = threshold;
                  old_threshold = threshold;
                  threshold = (threshold + max_threshold) / 2;       
                }    
                else { // Если меньше - понижаем порог
                  max_threshold = threshold;
                  old_threshold = threshold;   
                  threshold = (threshold + min_threshold) / 2;         
                } 
              }
              sum_threshold += threshold;   // Суммируем измерения   
            }
            
            mean_threshold = (float)sum_threshold/NUM_TH; // Усредняем измерения
            sum_threshold = 0;
            buf[bb] = mean_threshold;  // Накапливаем измерения в пакет
          }
          // Отправляем пакет в Serial
          for (bb = 0; bb < req_len; bb++) {
            Serial.print(buf[bb], 3);
            Serial.print('\n'); 
          }
          Serial.flush();  
          //Serial.print("Done");
        }
        break;
      }
      default: break;
    }

    // switch(Serial2.available() > 0){
    //   case true:
    //   {
    //     break;
    //   }
    //   default: break;
    // }
  }
  
}
