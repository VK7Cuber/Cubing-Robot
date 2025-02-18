#define DRIVER_STEP_TIME 1
#define GS_NO_ACCEL

#define echo_pin 44
#define trig_pin 42

#include "GyverStepper2.h"

// Пины перенастроить
GStepper2< STEPPER2WIRE> R_stepper(200 * 16, 8, 9, 10);
GStepper2< STEPPER2WIRE> F_stepper(200 * 16, 2, 3, 4);
GStepper2< STEPPER2WIRE> D_stepper(200 * 16, 38, 36, 34);
GStepper2< STEPPER2WIRE> U_stepper(200 * 16, 52, 50, 48);
GStepper2< STEPPER2WIRE> B_stepper(200 * 16, A8, A9, A10);
GStepper2< STEPPER2WIRE> L_stepper(200 * 16, A0, A1, A2);

// void U_turn(int degrees, int direction){
//   U_stepper.setTarget(direction * degrees, RELATIVE);
//   while (U_stepper.tick()){
//     continue;
//   }
//   U_stepper.brake();
// }


void U_turn(int degrees, int direction){
  D_stepper.brake();
  L_stepper.brake();
  F_stepper.brake();
  R_stepper.brake();
  B_stepper.brake();

  U_stepper.setTarget(direction * degrees, RELATIVE);
  while (U_stepper.tick()){
    continue;
  }
  U_stepper.brake();

  Serial.println(100);
}


void D_turn(int degrees, int direction){
  U_stepper.brake();
  L_stepper.brake();
  F_stepper.brake();
  R_stepper.brake();
  B_stepper.brake();

  D_stepper.setTarget(direction * degrees, RELATIVE);
  while (D_stepper.tick()){
    continue;
  }
  D_stepper.brake();

  Serial.println(100);
}


void L_turn(int degrees, int direction){
  U_stepper.brake();
  D_stepper.brake();
  F_stepper.brake();
  R_stepper.brake();
  B_stepper.brake();

  L_stepper.setTarget(direction * degrees, RELATIVE);
  while (L_stepper.tick()){
    continue;
  }
  L_stepper.brake();

  Serial.println(100);
}


void F_turn(int degrees, int direction){
  U_stepper.brake();
  D_stepper.brake();
  L_stepper.brake();
  R_stepper.brake();
  B_stepper.brake();

  F_stepper.setTarget(direction * degrees, RELATIVE);
  while (F_stepper.tick()){
    continue;
  }
  F_stepper.brake();

  Serial.println(100);
}


void R_turn(int degrees, int direction){
  U_stepper.brake();
  D_stepper.brake();
  L_stepper.brake();
  F_stepper.brake();
  B_stepper.brake();

  R_stepper.setTarget(direction * degrees, RELATIVE);
  while (R_stepper.tick()){
    continue;
  }
  R_stepper.brake();

  Serial.println(100);
}


void B_turn(int degrees, int direction){
  U_stepper.brake();
  D_stepper.brake();
  L_stepper.brake();
  F_stepper.brake();
  R_stepper.brake();
  
  B_stepper.setTarget(direction * degrees, RELATIVE);
  while (B_stepper.tick()){
    continue;
  }
  B_stepper.brake();
  
  Serial.println(100);

}


void set_start_position(){
  // откалибровать позиции
  U_stepper.brake();
  D_stepper.brake();
  L_stepper.brake();
  F_stepper.brake();
  R_stepper.brake();
  B_stepper.brake();

  int coefficient = 50 * 16;

  U_stepper.setTarget(200 * 16, ABSOLUTE);
  while (U_stepper.tick()){
    continue;
  }
  U_stepper.brake();

  D_stepper.setTarget(coefficient, ABSOLUTE);
  while (D_stepper.tick()){
    continue;
  }
  D_stepper.brake();

  L_stepper.setTarget(coefficient, ABSOLUTE);
  while (L_stepper.tick()){
    continue;
  }
  L_stepper.brake();

  F_stepper.setTarget(175 * 16, ABSOLUTE);
  while (F_stepper.tick()){
    continue;
  }
  F_stepper.brake();

  R_stepper.setTarget(coefficient, ABSOLUTE);
  while (R_stepper.tick()){
    continue;
  }
  R_stepper.brake();

  B_stepper.setTarget(175 * 16, ABSOLUTE);
  while (B_stepper.tick()){
    continue;
  }
  B_stepper.brake();





  
}

void setup_motors(){
  // U_stepper.setRunMode(FOLLOW_POS);
  // D_stepper.setRunMode(FOLLOW_POS);
  // L_stepper.setRunMode(FOLLOW_POS);
  // F_stepper.setRunMode(FOLLOW_POS);
  // R_stepper.setRunMode(FOLLOW_POS);
  // B_stepper.setRunMode(FOLLOW_POS);

  U_stepper.setMaxSpeed(3000);
  D_stepper.setMaxSpeed(3000);
  L_stepper.setMaxSpeed(3000);
  F_stepper.setMaxSpeed(3000);
  R_stepper.setMaxSpeed(3000);
  B_stepper.setMaxSpeed(3000);

  U_stepper.setAcceleration(0);
  D_stepper.setAcceleration(0);
  L_stepper.setAcceleration(0);
  F_stepper.setAcceleration(0);
  R_stepper.setAcceleration(0);
  B_stepper.setAcceleration(0);

  U_stepper.autoPower(true);
  D_stepper.autoPower(true);
  L_stepper.autoPower(true);
  F_stepper.autoPower(true);
  R_stepper.autoPower(true);
  B_stepper.autoPower(true);
}

void turn_motor(int turn){
  if (turn == 0) U_turn(50 * 16, -1);
  else if (turn == 1) D_turn(50 * 16, -1);
  else if (turn == 2) L_turn(50 * 16, -1);
  else if (turn == 3) F_turn(50 * 16, -1);
  else if (turn == 4) R_turn(50 * 16, -1);
  else if (turn == 5) B_turn(50 * 16, -1);

  else if (turn == 6) U_turn(50 * 16, 1);
  else if (turn == 7) D_turn(50 * 16, 1);
  else if (turn == 8) L_turn(50 * 16, 1);
  else if (turn == 9) F_turn(50 * 16, 1);
  else if (turn == 10) R_turn(50 * 16, 1);
  else if (turn == 11) B_turn(50 * 16, 1);

  else if (turn == 12) U_turn(100 * 16, 1);
  else if (turn == 13) D_turn(100 * 16, 1);
  else if (turn == 14) L_turn(100 * 16, 1);
  else if (turn == 15) F_turn(100 * 16, 1);
  else if (turn == 16) R_turn(100 * 16, 1);
  else if (turn == 17) B_turn(100 * 16, 1);
  
}

void change_speed_of_motors(int percents){
  int correct_percents = 255 - percents;
  float speed = correct_percents / 100.0 * 3000.0;
  U_stepper.setMaxSpeed(int(speed));
  D_stepper.setMaxSpeed(int(speed));
  L_stepper.setMaxSpeed(int(speed));
  F_stepper.setMaxSpeed(int(speed));
  R_stepper.setMaxSpeed(int(speed));
  B_stepper.setMaxSpeed(int(speed));

  U_stepper.brake();
  D_stepper.brake();
  L_stepper.brake();
  F_stepper.brake();
  R_stepper.brake();
  B_stepper.brake();

  Serial.println(int(speed));

}

int get_distance(){
  long t;
  long cm;

  digitalWrite(trig_pin, 0);
  delayMicroseconds(5);

  digitalWrite(trig_pin, 1);
  delayMicroseconds(10);
  digitalWrite(trig_pin, 0);

  t = pulseIn(echo_pin, 1);
  cm = t / 58.2;

  return cm;
}


void setup(){
  Serial.begin(9600);

  pinMode(trig_pin, OUTPUT);
  pinMode(echo_pin, INPUT);

  U_stepper.brake();
  D_stepper.brake();
  L_stepper.brake();
  F_stepper.brake();
  R_stepper.brake();
  B_stepper.brake();

  setup_motors();
  //set_start_position();

  U_stepper.brake();
  D_stepper.brake();
  L_stepper.brake();
  F_stepper.brake();
  R_stepper.brake();
  B_stepper.brake();

  Serial.write('1'); 
}

void loop(){ 
  if(Serial.available() > 0){
    int turn = Serial.read();
    if (get_distance() <= 13 or get_distance() > 100){
      if (turn > 90){
        change_speed_of_motors(turn);
      }
      else{ 
        turn_motor(turn); 
        Serial.println(turn);
      }
    }
    else {
      Serial.println(-1);
    }
  }
  //D_turn(50 * 16, 1);
}



