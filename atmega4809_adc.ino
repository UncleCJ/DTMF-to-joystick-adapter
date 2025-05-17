#include <avr/io.h>
#include <stdbool.h>

void ADC0_init(void);
void ADC0_start(void);
bool ADC0_done(void);
uint16_t ADC0_read(void);
void ADC0_stop(void);

void ADC0_init(void) {
  PORTD_PIN5CTRL &= ~PORT_ISC_gm;
  PORTD_PIN5CTRL |= PORT_ISC_INPUT_DISABLE_gc;
  PORTD_PIN5CTRL &= ~PORT_PULLUPEN_bm;
  ADC0.CTRLC = ADC_PRESC_DIV256_gc
             | ADC_REFSEL_VDDREF_gc;
              // | ADC_REFSEL_INTREF_gc;
  ADC0.CTRLA = ADC_ENABLE_bm
              | ADC_RESSEL_10BIT_gc;
  ADC0.MUXPOS = ADC_MUXPOS_AIN5_gc;
  ADC0.CTRLA |= ADC_FREERUN_bm;
}

void ADC0_start(void) {
  ADC0.COMMAND = ADC_STCONV_bm;
}

bool ADC0_done(void) {
  return (ADC0.INTFLAGS & ADC_RESRDY_bm);
}

uint16_t ADC0_read(void) {
  ADC0.INTFLAGS = ADC_RESRDY_bm;
  return ADC0.RES;
}

void ADC0_stop(void) {
  ADC0.COMMAND &= ~ADC_STCONV_bm;
}