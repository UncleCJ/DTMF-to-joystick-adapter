// atmega4809_adc.ino
void ADC0_init(void);
void ADC0_start(void);
bool ADC0_done(void);
uint16_t ADC0_read(void);
void ADC0_stop(void);

class Goertzel {
  public:
  Goertzel();
  Goertzel(float, float, int);
  void sample(void);
  float detect(void);
  void ProcessSample(uint16_t);

  private:  
  float sin_o;
  float cos_o;
  float C;
  float Q1;
  float Q2;
  void GetComplexResult(float*, float*);
  void Reset(void);
};

class HugoJoystick {
  public:
  HugoJoystick(int, int, int, int, int);
  void update(char);

  private:
  void release(int);
  void activate(int);
  void button_actuate(void (HugoJoystick::*)(int), char);
  void button_release(char);
  void button_activate(char);
  int UP, DOWN, LEFT, RIGHT, FIRE;
  char active, recent;
};

char DTMF_decode_magnitudes(float*);

// const int n = 481;  // 480 / 4.8 kHz = 100 ms
const int n = 120;  // ~25 ms, perhaps enough for 697 Hz (the longest period/lowest frequency)

Goertzel goertzels[7];

HugoJoystick joystick(9, 11, 5, 7, 3);


void setup() {
  // Columns 1209 (32) 1336 (35) 1477 (39) (1633)
  // Rows 697 (18, 676.125) 770 (20) 852 (22) 941 (25)
  Serial.begin(115200);
  ADC0_init();

  goertzels[0] = Goertzel(4808.0, 697.0, n);
  goertzels[1] = Goertzel(4808.0, 770.0, n);
  goertzels[2] = Goertzel(4808.0, 852.0, n);
  goertzels[3] = Goertzel(4808.0, 941.0, n);
  goertzels[4] = Goertzel(4808.0, 1209.0, n);
  goertzels[5] = Goertzel(4808.0, 1336.0, n);
  goertzels[6] = Goertzel(4808.0, 1477.0, n);
}

void loop() {
  uint16_t sample;
  float magnitudes[7];  // We are working with 7 DTMF tones, four rows + the three first columns

  ADC0_start();
  for (int i=0; i < n; i++) {
    while (1) {
      if (ADC0_done()) {
        sample = ADC0_read();
        break;
      }
    }

    for (int j=0; j < 7; j++) {
      goertzels[j].ProcessSample(sample);
    }
  }
  ADC0_stop();

  for (int j=0; j < 7; j++) {
    magnitudes[j] = goertzels[j].detect();
  }

  char decoded = DTMF_decode_magnitudes(magnitudes);
  Serial.println(decoded);
  joystick.update(decoded);

  // delay(2000);
}