
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
const int offTime = .000001;
const int onTime = .000001;

//Reading variable
int duration;

//--------------------------- Main Setup and Loop ------------------------------
void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

/*void loop() {
    
    duration = readSonar();
    
}*/

//--------------------------- Reading functions --------------------------------

void loop() {
    curMillis = micros();
    // Clears the trigPin for 1ms, then sets the trigPin on HIGH state for 10 ms
      digitalWrite(trigPin, trigState);
      if (curMillis - prevMillis  > offTime && trigState == LOW )
      {
        trigState = HIGH;
        digitalWrite(trigPin, trigState);
        prevMillis = curMillis;
      }
      else if (curMillis - prevMillis  > onTime && trigState == HIGH )
      {
        trigState = LOW;
        digitalWrite(trigPin, trigState);
        prevMillis = curMillis;
      }

    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    if (duration != 0){
    Serial.println(duration);
    }
}
