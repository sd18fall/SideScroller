/* Code running the InfraRed Sensors for [Team_Name]'s platformer game
* By Liz and Anya, 2018
* Requires an Arduino Uno and two Sharp IR sensors
* This is the debug-friendly version
*/


//--------------------------- Variable Setup -----------------------------------

//Calibration
float maxL; float maxR; float minL; float minR; float noneL; float noneR;
float calDiffL; float calDiffR;
int calCount = 0;
int calThresh = 50;

//Setup
const int IRL = A0;
const int IRR = A1;

//Take Reading
const int count = 5;
float reading;
float totReading;

//Capture and Print Reading
float distL;
float distR;
int toWhom;

//Inputs
String command;
int inputInt;

//Time control; not yet implemented
// unsigned long prevTime = millis();


//--------------------------- Main Setup and Loop ------------------------------
void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  pinMode(IRL, INPUT);
  pinMode(IRR, INPUT);

  calibrate();

  Serial.println("What are we reading out to? Accepted answers are: ");
  Serial.println("     '0' for csv, '1' for human, '2' for python");
  toWhom = getIntegerInput();

//--------------------------- Void Loop by Cases -------------------------------
  switch (toWhom) {
    case 1:
      Serial.println("At any time, enter any key to hang the program.");
      while(1) {
        readToHume();
        if (Serial.available()>0) {
          Serial.println("Waiting for another input to continue");
          getSilentInput();
        }
      }
    case 0:
      pS("R"); pSln("L");
      while(1) {readToCSV();}
    case 2:
      while(1) {readToPy();}
    }
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("----------lolimnotusingthis----------");
}


//--------------------------- "Read To" Loop functions -------------------------
void readToHume() {
  distL = readIR(IRL);
  distR = readIR(IRR);
  Serial.print("Readings are:    Left, ");
  Serial.print(distL);
  Serial.print("    Right, ");
  Serial.println(distR);

  delay(1000);
}

void readToCSV() {
  distL = readIR(IRL);
  distR = readIR(IRR);
  p(distL); pln(distR);

  delay(1000);
}

void readToPy() {
  distL = readIR(IRL);
  distR = readIR(IRR);
  p(distL); pln(distR);

  delay(1000);
}


//--------------------------- Calibration Function -----------------------------
void calibrate() {

//----------LeftMin----------
    Serial.println("Please hold your left hand at your comfortable lower limit");
    Serial.print("     ** Enter any key to take the reading.");
      getSilentInput();
    Serial.print(".");
      minL = readIR(IRL);
    Serial.println(".          Reading taken");


//----------LeftMax----------
    Serial.println("Please hold your left hand at your comfortable upper limit");
    Serial.print("     ** Enter any key to take the reading.");
      getSilentInput();
    Serial.print(".");
      maxL = readIR(IRL);
    Serial.println(".          Reading taken");

//----------RightMin----------
    Serial.println("Please hold your right hand at your comfortable lower limit");
    Serial.print("     ** Enter any key to take the reading.");
      getSilentInput();
    Serial.print(".");
      minR = readIR(IRR);
    Serial.println(".          Reading taken");

//----------RightMax----------
    Serial.println("Please hold your right hand at your comfortable upper limit");
    Serial.print("     ** Enter any key to take the reading.");
      getSilentInput();
    Serial.print(".");
      maxR = readIR(IRR);
    Serial.println(".          Reading taken");


//----------BothNone----------
    Serial.println("Please remove both of your hands from the sensors");
    Serial.print("     ** Enter any key to take the reading.");
      getSilentInput();
    Serial.print(".");
      noneL = readIR(IRL);
      noneR = readIR(IRR);
    Serial.println(".          Reading taken");


//----------Check and Re-Cal----------
    if (abs(maxR-noneR) < 50) {reCal(IRR);}
    if (abs(maxL-noneL) < 50) {reCal(IRL);}


//----------Diff and Print----------
    calDiffL = maxL - minL;
    calDiffR = maxR - minR;
    pS("MinL"); pS("   MinR"); pS("   MaxL"); pS("   MaxR"); pS("   DiffL"); pS("   DiffR"); pS("   noneL"); pSln("   noneR");
    p(minL); p(minR); p(maxL); p(maxR); p(calDiffL); p(calDiffR); p(noneL); pln(noneR);


    Serial.println("Calibration complete.");
    Serial.println("     ** Enter any key to continue.");
      getSilentInput();

}

void reCal(int pin) {
  calCount ++;

  pSln("");
  Serial.print("We couldn't tell the difference between no hand and your upper height on the ");
  if (pin == IRR) {Serial.println("right sensor.");}
  if (pin == IRL) {Serial.println("left sensor.");}

  if (calCount <= 2) {
  Serial.println("Please ensure your hand is directly over the sensor so it still sees you.");
  }
  if (calCount >= 1 && calCount <= 4) {
    Serial.println("Consider keeping your range smaller and lowering your upper limit.");
  }
  if (calCount >= 3) {
    Serial.println("Calibration is struggling. Consider repositioning the sensors or changing your lighting.");
    Serial.println("     Straight lines of movement and direct overhead lighting tends to produce better results.");
    Serial.println("Enter 'changing' if you are changing either of these; you will need to recalibrate from the beginning. Enter any other key(s) continue the single recalibration.");
      command = getOperatorInput();
    if (command = "changing") {
      calCount = 0;
      calibrate();
      return;
    }
  }

  pSln("");

  //----------BothNone----------
      Serial.println("Please remove both of your hands from the sensors");
      Serial.print("     ** Enter any key to take the reading.");
        getSilentInput();
      Serial.print(".");
        noneL = readIR(IRL);
        noneR = readIR(IRR);
      Serial.println(".          Reading taken");

  switch (pin) {
    case IRR:
    //----------RightMax----------
        Serial.println("Please hold your right hand at your comfortable upper limit");
        Serial.print("     ** Enter any key to take the reading.");
          getSilentInput();
        Serial.print(".");
          maxR = readIR(IRR);
        Serial.println(".          Reading taken");

        if (abs(maxR-noneR) < calThresh) {reCal(IRR);}

    case IRL:
    //----------LeftMax----------
        Serial.println("Please hold your left hand at your comfortable upper limit");
        Serial.print("     ** Enter any key to take the reading.");
          getSilentInput();
        Serial.print(".");
          maxL = readIR(IRL);
        Serial.println(".          Reading taken");

        if (abs(maxL-noneL) < calThresh) {reCal(IRL);}
  }
}


//---------------------------- Support Functions -------------------------------

int readIR(int pin) {
  //Take several readings and return the total
  reading = 0;
  totReading = 0;

  for (int i = 0; i < count; i++) {
      reading = analogRead(pin);

      totReading = reading + totReading;
      delay(1);
  }
  return totReading;
}


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
