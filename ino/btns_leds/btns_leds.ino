int leds [5] = {2, 3, 4, 5, 6};
int botones [5] = {7, 8, 9, 10, 11};

void setup() {
    for(int i = 0; i < 5; i++){
        pinMode(botones[i], INPUT_PULLUP);
        pinMode(leds[i], OUTPUT);
    }
    Serial.begin(9600);
    Serial.setTimeout(200);
}

int edosBtns [5]= {0, 0, 0, 0, 0};

void loop() {
    String cadena = "";
    
    for(int i = 0; i < 5; i++){
        edosBtns[i] = digitalRead(botones[i]);
        cadena += String(!edosBtns[i]);
        //digitalWrite(leds[i], !edosBtns[i]);
    }
    
    //  cadena += "\n";    
    Serial.println(cadena);

    delay(200);
}
