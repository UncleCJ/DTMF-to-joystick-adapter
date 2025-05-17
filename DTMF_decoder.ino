char DTMF_decode_magnitudes(float *magnitudes) {
  float sum = 0.0;
  int strongest_row, strongest_col;
  float strongest_magnitude = 0.0;

  for (int i = 0; i < 7; i++) {
    sum += magnitudes[i];
  }
  // Serial.println(sum/n);
  if (sum/n < 20.0) {
    return ' ';
  }
  
  for (int i=0; i < 4; i++) {
    if (magnitudes[i] > strongest_magnitude) {
      strongest_row = i;
      strongest_magnitude = magnitudes[i];
    }
  }
  strongest_magnitude = 0.0;
  for (int i=0; i < 3; i++) {
    if (magnitudes[i+4] > strongest_magnitude) {
      strongest_col = i;
      strongest_magnitude = magnitudes[i+4];
    }
  }

  switch (strongest_row) {
    case 0:
      switch (strongest_col) {
        case 0:
          return '1';
        case 1:
          return '2';
        case 2:
          return '3';
        default:
          return ' ';
      }
    case 1:
      switch (strongest_col) {
        case 0:
          return '4';
        case 1:
          return '5';
        case 2:
          return '6';
        default:
          return ' ';
      }
    case 2:
      switch (strongest_col) {
        case 0:
          return '7';
        case 1:
          return '8';
        case 2:
          return '9';
        default:
          return ' ';
      }
    case 3:
      switch (strongest_col) {
        case 0:
          return '*';
        case 1:
          return '0';
        case 2:
          return '#';
        default:
          return ' ';
      }
    default:
      return ' ';
  }
}
