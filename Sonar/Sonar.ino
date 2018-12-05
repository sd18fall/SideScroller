
/* Code running the Sonar Sensors for Brad the Bread
* By Liz and Anya, 2018
* Requires an Arduino Uno and a Sonar sensor
*/


//--------------------------- Variable Setup -----------------------------------

//Setup
const int sonarTrig = 3;
const int sonar = 2;

//Take and print Reading
int duration;


//--------------------------- Main Setup and Loop ------------------------------
void setup() {
  Serial.begin(9600);

  pinMode(sonarTrig, OUTPUT);
  pinMode(sonar, INPUT);
}

void loop() {
    send();
}


//--------------------------- Reading functions --------------------------------


void send() {
    duration = readSonar();
    pln(duration);
}

int readSonar() {
    // Clears the sonarTrig, then sets the sonarTrig on HIGH state for 10 micro seconds
      digitalWrite(sonarTrig, LOW);
      delayMicroseconds(2);
      digitalWrite(sonarTrig, HIGH);
      delayMicroseconds(10);
      digitalWrite(sonarTrig, LOW);

    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(sonar, HIGH);
    return duration;
}


void pln(int var) {Serial.println(var);}
