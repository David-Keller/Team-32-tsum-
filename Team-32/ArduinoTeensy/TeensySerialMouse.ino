
#define DEBUG 1

#define DEFAULT_X_SCREENSIZE 1440
#define DEFAULT_Y_SCREENSIZE 2560

#define LED 13

void blink(int d) {
  digitalWrite(LED, HIGH);
  delay(d);
  digitalWrite(LED, LOW);
  delay(150);
}

void blink() {
  blink(300);
}

bool toggled = false;
void toggle() {
  toggled = !toggled;
  digitalWrite(LED, toggled ? HIGH : LOW);
}

void setup() {
  pinMode(LED, HIGH);

  Serial3.begin(9600);
  Mouse.screenSize(DEFAULT_X_SCREENSIZE, DEFAULT_Y_SCREENSIZE);

  blink();
  blink();
}
/*
 * instead of parseInt()
 * loop read() (treating it like a state machine maybe in terms of handling the input)
 * until the end character then do the action
 */


int flag, state, x, y;
void loop() {
  if (Serial3.available()) {
    toggle(); // on

    if (DEBUG)
      Keyboard.print("Serial3.available(): " + Serial3.available());
    
    flag = Serial3.read();
    switch (flag) {
      case 'a': // set screen size
        x = Serial3.parseInt();
        y = Serial3.parseInt();

        Mouse.screenSize(x, y);

        break;
      case 'b': // move mouse
        x = Serial3.parseInt();
        y = Serial3.parseInt();

        Mouse.moveTo(x, y);

        break;
      case 'c': // click state
        state = Serial3.parseInt();

        if (state == 1)
          Mouse.press();
        else if (state == 0)
          Mouse.release();
        else if (state == 3)
          Mouse.click();

        break;
        case 'd': // type text
          auto text = Serial3.readString();
  
          Keyboard.print(text);
          break;
    }

    toggle(); // off
  }
}
