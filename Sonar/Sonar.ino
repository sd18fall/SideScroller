
/* Code running the InfraRed Sensors for [Team_Name]'s platformer game
* By Liz and Anya, 2018
* Requires an Arduino Uno and a Sonar sensor
*/


//--------------------------- Variable Setup -----------------------------------

//Calibration
float max; float min; float none; float calDiff;
int calCount = 0; int calThresh = 1;

//Setup
const int sonarTrig = 3;
const int sonar = 2;

//Take and print Reading
long duration;
float reading;
float dist;

//Inputs
String command;
int inputInt;


//--------------------------- Main Setup and Loop ------------------------------
void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  pinMode(sonarTrig, OUTPUT);
  pinMode(sonar, INPUT);

  // calibrate();
}

void loop() {
  // put your main code here, to run repeatedly:
    send();
}


//--------------------------- Reading functions --------------------------------

void readOut() {
    dist = readSonar(); pln(dist);
    delay(500);
}

void send() {
    dist = readSonar();
    pln(dist);
}

int readSonar() {
  //Take several readings and return the total
    reading = 0;

    // Clears the sonarTrig, then sets the sonarTrig on HIGH state for 10 micro seconds
      digitalWrite(sonarTrig, LOW);
      delayMicroseconds(2);
      digitalWrite(sonarTrig, HIGH);
      delayMicroseconds(10);
      digitalWrite(sonarTrig, LOW);

    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(sonar, HIGH);

    // Calculating and return the distance
    // reading = duration*0.034/2;
    return duration;
}



//--------------------------- Calibration Function -----------------------------
void calibrate() {

//----------Min----------
    Serial.println("Please hold your hand at your comfortable lower limit");
    Serial.print("     ** Enter any key to take the reading.");
      getSilentInput();
    Serial.print(".");
      min = readSonar();
    Serial.println(".          Reading taken");


//----------Max----------
    Serial.println("Please hold your hand at your comfortable upper limit");
    Serial.print("     ** Enter any key to take the reading.");
      getSilentInput();
    Serial.print(".");
      max = readSonar();
    Serial.println(".          Reading taken");


//----------BothNone----------
    Serial.println("Please remove both of your hands from the sensor");
    Serial.print("     ** Enter any key to take the reading.");
      getSilentInput();
    Serial.print(".");
      none = readSonar();
    Serial.println(".          Reading taken");


//----------Check and Re-Cal----------
    if (abs(max-none) < calThresh) {reCal(); calibrate(); return;}


//----------Diff and Print----------
    calDiff = max - min;
    pS("Min"); pS("   Max"); pS("   Diff"); pSln("   none");
    p(min); p(max); p(calDiff); pln(none);


    Serial.println("Calibration complete.");
    Serial.println("     ** Enter any key to continue.");
      getSilentInput();

}

void reCal() {
  calCount ++;

  pSln("");
  Serial.print("We couldn't tell the difference between no hand and your upper height.");

//Variable instructions
  if (calCount <= 2) {
  Serial.println("Please ensure your hand is directly over the sensor so it still sees you.");
  }
  if (calCount >= 1 && calCount <= 4) {
    Serial.println("Consider keeping your range smaller and lowering your upper limit.");
  }
  if (calCount >= 3) {
    Serial.println("Calibration is struggling. Consider repositioning the sensors or changing your lighting.");
    Serial.println("     Straight lines of movement and direct overhead lighting tends to produce better results.");
    // Serial.println("Enter 'changing' if you are changing either of these; you will need to recalibrate from the beginning. Enter any other key(s) continue the single recalibration.");
    //   command = getOperatorInput();
    // if (command = "changing") {
    //   calCount = 0;
    //   calibrate();
    //   return;
    // }
  }
}


//---------------------------- Support Functions -------------------------------

void p(float var) {Serial.print(var); Serial.print(",     ");}

void pln(float var) {Serial.println(var);}

void pS(String var) {Serial.print(var); Serial.print(",     ");}

void pSln(String var) {Serial.println(var);}


//--------------------------- "Get Input" Functions ----------------------------

String getOperatorInput() {
  // This function prompts, waits for, parses, and returns a string input
  Serial.println("     ** Offer a command input");
  while (Serial.available()==0) {};                     // do nothing until operator input typed
  command = Serial.readString();                        // read command string
  Serial.print("     Input Recieved:  "); // give command feedback to operator
  Serial.println(command);
  return command;
}

String getSilentInput() {
  // This function gets and parses a string input without printing anything
  while (Serial.available()==0) {};                     // do nothing until operator input typed
  command = Serial.readString();                        // read command string
  return command;
}

int getIntegerInput() {
  // This function prompts for, waits for, parses, and returns an integer input

  Serial.println("     ** Offer an integer input:");
  while (Serial.available()==0) {};                     // do nothing until operator input typed
  inputInt = Serial.parseInt();                        // read command string
  return inputInt;
}
