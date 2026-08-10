#define ENA 5
#define IN1 7
#define IN2 8
#define ENB 6
#define IN3 9
#define IN4 10
int motorSpeed = 180; 
void setup() {
pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
pinMode(ENB, OUTPUT); pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
stopMotors();
Serial.begin(9600);
}
void loop() {
if (Serial.available() > 0) {
char command = Serial.read();
switch (command) {
  case 'F': forward(); break;
  case 'B': backward(); break;
  case 'R': rightTurn(); break;
  case 'S': stopMotors(); break;
  default: stopMotors(); break;
}
}
}
void forward() {
digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
analogWrite(ENA, motorSpeed);
digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
analogWrite(ENB, motorSpeed);
}
void backward() {
digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
analogWrite(ENA, motorSpeed);
digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
analogWrite(ENB, motorSpeed);
}
void rightTurn() {
digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
analogWrite(ENA, motorSpeed);
digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
analogWrite(ENB, motorSpeed);
}
void stopMotors() {
analogWrite(ENA, 0); analogWrite(ENB, 0);
digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}
