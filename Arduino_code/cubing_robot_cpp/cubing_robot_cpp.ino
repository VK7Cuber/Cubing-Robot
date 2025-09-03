#define DRIVER_STEP_TIME 1
#define GS_NO_ACCEL

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

int CURRENT_SPEED = -1;
float MAX_SPEED = 7000.0;

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

// New dual-motor simultaneous turns
void UD_turn(int U_degrees, int U_direction, int D_degrees, int D_direction){
  // Brake other axes
  L_stepper.brake();
  F_stepper.brake();
  R_stepper.brake();
  B_stepper.brake();

  U_stepper.setTarget(U_direction * U_degrees, RELATIVE);
  D_stepper.setTarget(D_direction * D_degrees, RELATIVE);
  while (U_stepper.tick() | D_stepper.tick()){
    continue;
  }
  U_stepper.brake();
  D_stepper.brake();

  Serial.println(100);
}

void FB_turn(int F_degrees, int F_direction, int B_degrees, int B_direction){
  // Brake other axes
  U_stepper.brake();
  D_stepper.brake();
  L_stepper.brake();
  R_stepper.brake();

  F_stepper.setTarget(F_direction * F_degrees, RELATIVE);
  B_stepper.setTarget(B_direction * B_degrees, RELATIVE);
  while (F_stepper.tick() | B_stepper.tick()){
    continue;
  }
  F_stepper.brake();
  B_stepper.brake();

  Serial.println(100);
}

void LR_turn(int L_degrees, int L_direction, int R_degrees, int R_direction){
  // Brake other axes
  U_stepper.brake();
  D_stepper.brake();
  F_stepper.brake();
  B_stepper.brake();

  L_stepper.setTarget(L_direction * L_degrees, RELATIVE);
  R_stepper.setTarget(R_direction * R_degrees, RELATIVE);
  while (L_stepper.tick() | R_stepper.tick()){
    continue;
  }
  L_stepper.brake();
  R_stepper.brake();

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

  U_stepper.setMaxSpeed(int(MAX_SPEED));
  D_stepper.setMaxSpeed(int(MAX_SPEED));
  L_stepper.setMaxSpeed(int(MAX_SPEED));
  F_stepper.setMaxSpeed(int(MAX_SPEED));
  R_stepper.setMaxSpeed(int(MAX_SPEED));
  B_stepper.setMaxSpeed(int(MAX_SPEED));

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

  // Dual-axis turns based on encoding 18..44
  else if (turn == 18) UD_turn(50 * 16, -1, 50 * 16, -1);      // UD
  else if (turn == 19) UD_turn(50 * 16, -1, 50 * 16, 1);       // UD'
  else if (turn == 20) UD_turn(50 * 16, -1, 100 * 16, 1);      // UD2
  else if (turn == 21) UD_turn(50 * 16, 1, 50 * 16, -1);       // U'D
  else if (turn == 22) UD_turn(50 * 16, 1, 50 * 16, 1);        // U'D'
  else if (turn == 23) UD_turn(50 * 16, 1, 100 * 16, 1);       // U'D2
  else if (turn == 24) UD_turn(100 * 16, 1, 50 * 16, -1);      // U2D
  else if (turn == 25) UD_turn(100 * 16, 1, 50 * 16, 1);       // U2D'
  else if (turn == 26) UD_turn(100 * 16, 1, 100 * 16, 1);      // U2D2

  else if (turn == 27) FB_turn(50 * 16, -1, 50 * 16, -1);      // FB
  else if (turn == 28) FB_turn(50 * 16, -1, 50 * 16, 1);       // FB'
  else if (turn == 29) FB_turn(50 * 16, -1, 100 * 16, 1);      // FB2
  else if (turn == 30) FB_turn(50 * 16, 1, 50 * 16, -1);       // F'B
  else if (turn == 31) FB_turn(50 * 16, 1, 50 * 16, 1);        // F'B'
  else if (turn == 32) FB_turn(50 * 16, 1, 100 * 16, 1);       // F'B2
  else if (turn == 33) FB_turn(100 * 16, 1, 50 * 16, -1);      // F2B
  else if (turn == 34) FB_turn(100 * 16, 1, 50 * 16, 1);       // F2B'
  else if (turn == 35) FB_turn(100 * 16, 1, 100 * 16, 1);      // F2B2

  else if (turn == 36) LR_turn(50 * 16, -1, 50 * 16, -1);      // LR
  else if (turn == 37) LR_turn(50 * 16, -1, 50 * 16, 1);       // LR'
  else if (turn == 38) LR_turn(50 * 16, -1, 100 * 16, 1);      // LR2
  else if (turn == 39) LR_turn(50 * 16, 1, 50 * 16, -1);       // L'R
  else if (turn == 40) LR_turn(50 * 16, 1, 50 * 16, 1);        // L'R'
  else if (turn == 41) LR_turn(50 * 16, 1, 100 * 16, 1);       // L'R2
  else if (turn == 42) LR_turn(100 * 16, 1, 50 * 16, -1);      // L2R
  else if (turn == 43) LR_turn(100 * 16, 1, 50 * 16, 1);       // L2R'
  else if (turn == 44) LR_turn(100 * 16, 1, 100 * 16, 1);      // L2R2
  
}

void change_speed_of_motors(int percents){
  int correct_percents = 255 - percents;
  float speed = correct_percents / 100.0 * MAX_SPEED;
  int int_speed = int(speed);
  if (int_speed != CURRENT_SPEED) {
    CURRENT_SPEED = int_speed;

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
  }
  Serial.println(int_speed);

}


void setup(){
  Serial.begin(9600);

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
    if (turn > 90){
      change_speed_of_motors(turn);
    }
    else{ 
      turn_motor(turn); 
      Serial.println(turn);
    }
  }
  //D_turn(50 * 16, 1);
}