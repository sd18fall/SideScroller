
/* Code running the Sonar Sensors for Brad the Bread
* By Liz and Anya, 2018
* Requires an Arduino Uno and a Sonar sensor
*/


//--------------------------- Variable Setup -----------------------------------

//Setup
const int trigPin = 3;
const int echoPin = 2;
bool trigState = LOW;

int duration;
/*
int trigState = LOW;
//Take and print Reading
int duration, distance; //variables
int interval = 1; // interval in milliseconds at which trigPin turns on
int interval2 = 1000; //time in milliseconds at which the distance is printed in serial monitors
int printState = LOW; //whether or not to print distance
unsigned long currentMillis;
unsigned long previousMillis = 0; //microsecond at which the pin was last writen

unsigned long curMillis;
unsigned long prevmillis = 0;
*/

//--------------------------- Main Setup and Loop ------------------------------
void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
    curMillis = millis()
    duration = readSonar();
    pln(duration);
    prevMillis = curMillis;
}

//--------------------------- Reading functions --------------------------------

int readSonar() {
    // Clears the trigPin, then sets the trigPin on HIGH state for 10 micro seconds
      digitalWrite(trigPin, LOW);
      if (curMillis - prevMillis && trigPin =  > 1000)
      {
        digitalWrite(trigPin, HIGH);
      }
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);

    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    return duration;
}


void pln(int var) {Serial.println(var);}

/*
//---------------I DONT UNDERSTAND----------!!!!!!!!!!!!!!!!!!!!!!
void loop() {
    // Clears the trigPin, then sets the trigPin on HIGH state for 10 micro seconds
  currentMillis = millis(); //time in milliseconds from which the code was started

  if (currentMillis-previousMillis >= interval) { //check "blink without delay" code
		previousMillis = currentMillis;
		if (trigState == LOW){
			(trigState = HIGH);
		}
		else {
			(trigState = LOW);
		}
	}
	// printing if statement
	if (currentMillis-previousMillis >= interval2) { //check "blink without delay" code
		previousMillis = currentMillis;
		if (printState == LOW){
			(printState = HIGH);
		}
		else {
			(printState = LOW);
		}
	}
	digitalWrite(trigPin,trigState);
	duration = pulseIn(echoPin,HIGH);

	if (printState = HIGH and duration != 0){
	  Serial.println(duration);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    //return duration;

}
}
//----------------END Not getting it--------------!!!!!!!!!!!!!!!!!
*/
