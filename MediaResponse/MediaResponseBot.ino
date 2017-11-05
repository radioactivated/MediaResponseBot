#include <Servo.h>

#define LARM_PIN 10
#define RARM_PIN 11

Servo lArm;
Servo rArm;

volatile boolean flailing = false;


void setup() {
  lArm.attach(LARM_PIN);
  rArm.attach(RARM_PIN);
  
  Serial.begin(9600);
  
  
}

void loop() {
  if(Serial.available()) {  
    String command = Serial.readString();
    if(command.indexOf("twote") >= 0) {
       if(!flailing) flail(); 
    }
  }
  delay(10);
}

void flail() {
  flailing = true;
  for(int i = 0; i < 8; i++) {
    lArm.write(180);
    rArm.write(180);
    delay(500);
    lArm.write(0);
    rArm.write(0);
    delay(500);
  }
  delay(1000);
  flailing = false;
}
