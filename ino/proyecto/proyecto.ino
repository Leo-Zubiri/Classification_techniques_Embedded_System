int i;
const int leds[8] = {6, 7, 8, 9, 10, 11, 12, 13};
const int ptms[8] = {A0,A1,A2,A3,A4,A5,A6,A7};
String lectura;

void setup() {
  // put your setup code here, to run once:
    for (i  = 0; i < 8; i++) {
    pinMode(leds[i], OUTPUT);
  }

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  lectura = "";

  for(i=0; i< 8;i++){
    lectura+= String(analogRead(ptms[i]))+" ";
  }

  Serial.println(lectura);

  delay(200);
}
