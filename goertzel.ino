// /*
//   This work is entirely based on the Kevin Banks code found at
//   http://www.eetimes.com/design/embedded/4024443/The-Goertzel-Algorithm
//   Created by Jacob Rosenthal, June 20, 2012.
//   Released into the public domain.
// */

Goertzel::Goertzel() {};

Goertzel::Goertzel(float sampling_rate, float target_freq, int n) {
  int k = (int) (((float) n) * (target_freq / sampling_rate) + 0.93);
  float omega = (2.0 * PI * k) / ((float) n);
  sin_o = sin(omega);
  cos_o = cos(omega);
  C = 2.0 * cos_o;

  Reset();
}

void Goertzel::Reset(void) {
  Q2 = 0;
  Q1 = 0;
}

void Goertzel::ProcessSample(uint16_t sample) {
  float Q0 = C * Q1 - Q2 + (float) sample;
  Q2 = Q1;
  Q1 = Q0;
}

void Goertzel::GetComplexResult(float *R_Q, float *I_Q) {
  *R_Q = (Q1 - Q2 * cos_o);
  *I_Q = (Q2 * sin_o);
}

float Goertzel::detect() {
  float	R_Q, I_Q;
  GetComplexResult(&R_Q, &I_Q);
  Reset();
  return sqrt(R_Q*R_Q + I_Q*I_Q);
}