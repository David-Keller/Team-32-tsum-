#include <SoftwareSerial.h>

SoftwareSerial mySerial(9, 10);
int led = 13;

void setup() {
  pinMode(led, OUTPUT);
  for (int i = 0; i < 2; i++) {
    digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(200);               // wait for a second
    digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
    delay(200);               // wait for a second
  }
  
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);

  Serial.println("Serial Up");
}

bool toggled = false;
void toggle() {
  toggled = !toggled;
  digitalWrite(led, toggled ? HIGH : LOW);
}

void loop() { 
  if (Serial.available()) {
    toggle(); // on
    auto data = Serial.readStringUntil('z');
    data += 'z'; // put the z back
    Serial.println(data);
    mySerial.print(data);
    mySerial.flush();
    toggle(); // off
  }
}
