
/* Code running the Sonar Sensors for Brad the Bread game
*    By Liz and Anya, 2018
*    Requires a sonar sensor
*/


//--------------------------- Variable Setup -----------------------------------
//Setup
const int trigPin = 3;
const int echoPin = 2;

//Cycle trigger with non-delay timers
unsigned long curMillis;
unsigned long prevMillis = 0;
bool trigState = LOW;
const int offTime = 1;
const int onTime = 10;

//Reading variable
int duration;

//--------------------------- Main Setup and Loop ------------------------------
void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
    curMillis = millis();
    duration = readSonar();
    Seial.println(duration);
}

//--------------------------- Reading functions --------------------------------

int readSonar() {
    // Clears the trigPin for 1ms, then sets the trigPin on HIGH state for 10 ms
      digitalWrite(trigPin, trigState);
      if (curMillis - prevMillis && trigState == LOW  > offTime)
      {
        trigState = HIGH;
        digitalWrite(trigPin, trigState);
        prevMillis = curMillis;
      }
      else if (curMillis - prevMillis && trigState == HIGH  > onTime)
      {
        trigState = LOW;
        digitalWrite(trigPin, trigState);
        prevMillis = curMillis;
      }

    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    return duration;
}
