void HugoJoystick::release(int pin) {
  pinMode(pin, INPUT);
}

void HugoJoystick::activate(int pin) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
}

void HugoJoystick::button_actuate(void (HugoJoystick::*actuator)(int), char button) {
  switch (button) {
    case '4':
      (this->*actuator)(LEFT);
      break;
    case '5':
      (this->*actuator)(UP);
      break;
    case '6':
      (this->*actuator)(RIGHT);
      break;
    case '9':
      (this->*actuator)(RIGHT);
      (this->*actuator)(UP);
      break;
    case '8':
      (this->*actuator)(DOWN);
      break;
    case '0':
      (this->*actuator)(FIRE);
      break;
    default:
      break;
  }

}

void HugoJoystick::button_release(char button) {
  button_actuate(&HugoJoystick::release, button);
}


void HugoJoystick::button_activate(char button) {
  button_actuate(&HugoJoystick::activate, button);
}

HugoJoystick::HugoJoystick(int up, int down, int right, int left, int fire)
    : UP(up), 
      DOWN(down), 
      LEFT(left), 
      RIGHT(right),
      FIRE(fire) {   
  int pins[] = {UP, DOWN, LEFT, RIGHT, FIRE};
  for (int pin : pins) {
    release(pin);
  }
  active = ' ';
  recent = ' ';
}

void HugoJoystick::update(char current) {
  if (current != '4'
        && current != '5'
        && current != '6' 
        && current != '8'
        && current != '9'
        && current != '0') { // current is not a valid joystick input
    if (active == ' ' || recent != ' ') {
      recent = ' ';
      return;
    }
    else { // active != ' ' && recent == ' '
      button_release(active);
      active = ' ';
      return;
    }
  }
  else { // current is a valid joystick input
    if (active == current
        || recent != current) {
      recent = current;
      return;
    }
    else { // active != current && recent == current
      button_release(active);
      button_activate(current);
      active = current;
      return;
    }
  }   
}