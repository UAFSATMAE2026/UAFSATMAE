#include "CytronMotorDriver.h"

const long heartbeat = 16;
unsigned long premillis = 0;

CytronMD motor1(PWM_DIR, 4, 7); // Motor 1. PWM pin is 8, DIR pin is 5 Front Left. Negative to go forward
CytronMD motor2(PWM_DIR, 6, 3);   // Motor 2. PWM pin is 9, DIR pin is 4 Back Right negative to go forward
CytronMD motor3(PWM_DIR, 9, 13);   // Motor 3. PWM pin is 10, DIR pin is 3 Front Right positive to forward
CytronMD motor4(PWM_DIR, 11, 12);   // Motor 4. PWM pin is 11, DIR pin is 2 Back Left Positive to forward


void setup() {
  Serial.begin(115200); // reading bits at 115200 times a second
}

void loop() {
  unsigned long currentMillis = millis();
  // My big ol encompassing if statement that checks to see if the serial connection has any data coming through.
  if(Serial.available() > 0 && currentMillis - premillis >= heartbeat){
    premillis = currentMillis;
    int x = Serial.parseInt();
    int y = Serial.parseInt();
    int align = Serial.parseInt();

    if( ( -20 < x && x < 20) && ( -20 < y && y < 20) ){ // deadzone stop
      motorSpeed(0, 0, 0, 0);
    }
    else if( (-45 < x && x < 45) && (y > 45) ){ // straight forward
      motorSpeed(128, 128, 128, 128);
    }
    else if( (-45 < x && x < 45) && (y < -45) ){ // straight backwards
      motorSpeed(-128, -128, -128, -128);
    }
    else if(align == 1){
      if( (x > 45) && (-45 < y && y < 45) ){ // sideways right
        motorSpeed(-128, -128, 128, 128);
      }
      else if( (x < -45) && (-45 < y && y < 45) ){ // sideways left
        motorSpeed(128, 128, -128, -128);
      }
    }
    else if(align == 0){
      if( (x > 45) && (-45 < y && y < 45) ){ // spin right
        motorSpeed(128, -128, 128, -128);
      }
      else if( (x < -45) && (-45 < y && y < 45) ){ // spin left
        motorSpeed(-128, 128, -128, 128);
      }
    }
//    if(){ // diagonal right
//      motorSpeed(128, 0, 0, 128);
//    }
//    if(){ // diagonal left
//      motorSpeed(0, 128, 128, 0);
//    }
//    if(){ // diagonal back-right 
//      motorSpeed(-128, 0, 0, -128);
//    }
//    if(){ // diagonal back-left 
//      motorSpeed(0, -128, -128, 0);
//    }
//    if(){ // concerning right
//      motorSpeed(128, 0, 128, 0);
//    } 
//    if(){ // concerning left
//      motorSpeed(0, 128, 0, 128);
//    } 
//    if(){ // turn around right
//      motorSpeed(128, -128, 128, -128);
//    } 
//    if(){ // turn around left
//      motorSpeed(-128, 128, -128, 128);
//    } 
//    if(){ // stop
//      motorSpeed(0, 0, 0, 0);
//    }
  }
}
void motorSpeed(int motorSpeed1, int motorSpeed2, int motorSpeed3, int motorSpeed4){
  motor1.setSpeed(motorSpeed1);
  motor2.setSpeed(motorSpeed2);
  motor3.setSpeed(motorSpeed3);
  motor4.setSpeed(motorSpeed4);
}
