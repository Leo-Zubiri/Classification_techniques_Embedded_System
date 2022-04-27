int i;
const int leds[5] = {2,3,4,5,6};
const int ptms[13] = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12};
String lectura;

void setup() {
  // put your setup code here, to run once:
    for (i  = 0; i < 5; i++) {
    pinMode(leds[i], OUTPUT);
  }

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  lectura = "";

  for(i=0; i < 12;i++){
    lectura+= String(analogRead(ptms[i]))+",";
  }
  lectura+= String(analogRead(ptms[i]));
  Serial.println(lectura);

  delay(200);
}
