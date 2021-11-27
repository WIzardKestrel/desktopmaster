int ledPin[] = {4,5,6,7,8,9,10,11,12,13}; // the pin that the LED is attached to
int sound_lvl;
int cont_lvl;
int pot_pin = A1;
int old_vol_lvl = 0;
void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  // initialize the LED pin as an output:
  for (int i = 13; i > 3; i--) {
    pinMode(i, OUTPUT);
  }
}


void loop() {

  cont_lvl = (analogRead(pot_pin));
  if (abs(cont_lvl - old_vol_lvl) > 30) {
    old_vol_lvl = cont_lvl;
    Serial.println(cont_lvl);
  }else{
      
  }

  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    sound_lvl = Serial.read();
    if (sound_lvl == ' ' || sound_lvl == '\n')
      ;
    else {
      //Serial.print('\n');
      switch (sound_lvl) {
        case '0':
          turn_on(10);
          break;
        case '1':
          turn_on(1);
          break;

        case '2':
          turn_on(2);
          break;

        case '3':
          turn_on(3);
          break;

        case '4':
          turn_on(4);
          break;

        case '5':
          turn_on(5);
          break;

        case '6':
          turn_on(6);
          break;

        case '7':
          turn_on(7);
          break;

        case '8':
          turn_on(8);
          break;

        case '9':
          turn_on(9);
          break;
      }
    }
  }
}

void turn_on(int level) {
  for (int i = 0; i < level; i++) {
    digitalWrite(ledPin[i], HIGH);
  }
  for (int i = 14; i >= level; i--) {
    digitalWrite(ledPin[i], LOW);
   }
}
// // the pin that the LED is attached to
//int sound_level;      // a variable to read incoming serial data into
//
//void setup() {
//  // initialize serial communication:
//  Serial.begin(9600);
//  // initialize the LED pin as an output:

//}
//
//void loop() {
//
//  if (Serial.available() > 0) {
//    // read the oldest byte in the serial buffer:
//    sound_level = Serial.read();
//    printf("sound: %d\n", sound_level);

//}
