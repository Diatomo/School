


/*
   Roto
 
 Project:FRIST
 Exhibit: Sound Vibration
 Author(s): Charles Stevenson
 Date: 1/24/18
 
 Original environment:
 Arduino 1.8.2
 
 Revision notes:
 
 */


#include "alarmClock.h"
#include "digits.h"
#include "outputExtend.h"

#define versionString "Roto - [FRIST] [Sound Vibration]"

//sizes
uint8_t const NUM_HERTZ = 7;
uint8_t const NUM_OE = 1;
uint8_t const NUM_SEGS = 4;
uint8_t const NUM_CLOCKS = 3;
uint8_t const NUM_STATES = NUM_CLOCKS;
uint8_t const OE_OFFSET = 1;
uint32_t const COUNTER_MAX = 10000; //FOR KNOB (sorry about poor naming conventions.)
uint8_t const MAX_COUNTS = 20; //FOR CLEANUP


//settings
uint32_t const BAUD_RATE = 9600;
uint8_t currHertz = 1;
uint8_t prevHertz = 1;
uint8_t blowCounter = 0;
uint32_t const displayHertz[NUM_HERTZ] = {853,1125,1386,1518,1711,1834,2194};


//states
bool activeState = false;
bool chaserState = true;
bool blowerState = false;
bool* states[NUM_STATES] = {&activeState, &chaserState, &blowerState};

bool hzChange = false;


//sound only plays when inactive for a certain period of time;
bool activeKnob = false;//boolean to check to see if knob is in action;
uint32_t activeKnobTimer = 0;
uint32_t knobTimerInterval = 2000;

//counters
int hertzCounter = COUNTER_MAX/2;

//pin configurations
uint32_t const oeData = 13;
uint32_t const oeClock = 12;
uint32_t const oeLatch = 11;
uint32_t const segData = 17;
uint32_t const segClock = 18;
uint32_t const segLatch = 19;
uint32_t const chanA = 2;
uint32_t const chanB = 3;

//prototypes
void resetExhibit();
void sexify();
void turnOffBlower();

//init clocks
alarmClock resetClk = alarmClock(resetExhibit);
alarmClock attractClk = alarmClock(sexify);
alarmClock termBlowerClk = alarmClock(turnOffBlower);

//define timers
uint32_t resetTimer = 60000;
uint32_t chaseTimer = 300;
uint32_t blowTimer = 10000;

alarmClock clocks[NUM_CLOCKS] = {resetClk, attractClk, termBlowerClk};
uint32_t const timers[NUM_CLOCKS] = {resetTimer, chaseTimer, blowTimer};

outputExtend oe = outputExtend(oeData, oeClock, oeLatch, NUM_OE); 
digits dig = digits(segData, segClock, segLatch, NUM_SEGS);
digitGroup segs = digitGroup(&dig, 0, NUM_SEGS); 

/* =========    INITIAL SETUP    ================*/
/*
*
*	FxN :: setupSegs
*		protocol to reset pins on 7segs
*
*/
void setupSegs(){
		for (byte i = segData; i <= segLatch; i++){
				digitalWrite(i,LOW);			
		}
		for (byte i = segData; i < segLatch; i++){
				digitalWrite(i,HIGH);
		}
}

void setupOE(){
		//oe Extended.
		for (byte i = 0; i < NUM_HERTZ + OE_OFFSET; i++){
				oe.extendedWrite(i,LOW);
				delay(100);
		}
}

/*
*
* FxN :: setup
*
*
*/
void setup(){
		
		//Open Serial && write version
		Serial.begin(BAUD_RATE);
		Serial.println(versionString);
		Serial.print(F("File: "));
		Serial.println(__FILE__);

		//pins
		pinMode(chanA, INPUT);
		pinMode(chanB, INPUT);

		//interrupt
		attachInterrupt(digitalPinToInterrupt(2),changeHertz,CHANGE); 

		//setupBoards
		setupSegs();
		setupOE();
}

/* =========    HELPER FUNCTIONS    ================*/

/*
*
*  FxN :: sexify
*   Attraction Function
*
*/
void sexify(){
    segs.chaseAnimation8();//sexy chase animation
}

/*
*
* FxN :: resetExhibit
*	resets certain parameters to an initial state
*
*/
void resetExhibit(){
		currHertz = 1;
		prevHertz = 1;
		hertzCounter = COUNTER_MAX/2;
		activeState = false;
		chaserState = !activeState;
		blowerState = false;
}

/*
*
*  FxN :: playSound
*   Routine that plays sound.
*
*/
void playSound(){
    oe.extendedWrite(currHertz + OE_OFFSET, HIGH);//reset
    delay(1000);//wait to register
    oe.extendedWrite(currHertz + OE_OFFSET, LOW);//play sound
    delay(100);
    blowCounter++;
}


/*
*
* FxN :: turnOnBlower
*   Turns on the blower (untimed)
*
*/
void turnOnBlower(){
    oe.extendedWrite(0,LOW);
    delay(100);
    oe.extendedWrite(0,HIGH);
    delay(100);

}

/*
*
* FxN :: turnOffBlower()
*   Timed function, turns blower off.
*
*/
void turnOffBlower(){
    oe.extendedWrite(0,HIGH);
    delay(100);
    oe.extendedWrite(0,LOW);
    delay(100);
    resetExhibit();
} 


/* =========    KNOB STATS    ================*/

/*
*
*
*	FxN :: changeHertz
*		Interrupt Function, that counts up and down the encoder values.
*
*/
void changeHertz(){
		if (digitalRead(chanA) != digitalRead(chanB)){
				if (hertzCounter < COUNTER_MAX && (currHertz < (NUM_HERTZ-1))){ //increment if hertzCounter < MAX && currInterval is not maxed;
						hertzCounter++;
				}
		}
		else{
				if (hertzCounter > 0 && (currHertz > 0)){
						hertzCounter--;
				}
		}
}

/*
*
*	FxN :: analyzeHertz
*		Analyzes is a change needs to be made to the overall hertz		
*
*
*/
boolean analyzeHertz(){
		boolean change = false;
		if (hertzCounter >= COUNTER_MAX){
				if (currHertz < (NUM_HERTZ - 1)){
						currHertz++;
            hzChange = true; //lazy but important edit
						change = true;
				}
		}
		else if (hertzCounter <= 0){
				if (currHertz > 0){
						currHertz--;
            hzChange = true; //lazy but important edit
						change = true;
				}
		}
		return change;
}

/*
*
*	FxN :: checkCleanUp
*		checks if sand needs to be reblown and switched to corresponding state
*
*/
void checkCleanUp(){
		if (blowCounter == MAX_COUNTS){
				activeState = false;
				chaserState = true;
				blowerState = true;
				blowCounter = 0;
				turnOnBlower();
		}
}

/*
*
*	FxN :: knobInactive
*		Specific logic checking if the knob has been touched
*	
*
*/
bool knobInactive(){
		bool trigger = false;
		if (activeKnob == false){
				if (activeKnobTimer == 0){
						activeKnobTimer = millis();
				}
				else{
						trigger = pKaDuration();
				}
		}
		else{
				activeKnobTimer = 0;
		}
		return trigger;
}

/*
*
*	FxN :: pKaDuration
*		aka Knob Duration. If its been for the allotted time send a trigger (pka);
*
*/
bool pKaDuration(){
		bool pKa = false;
		if (millis() - activeKnobTimer > knobTimerInterval){
				pKa = true;
				activeKnobTimer = 0;
		}
		return pKa;
}


/* =========    STATE LOGIC FLOW CONTROLLERS    ================*/


/*
*
*	FxN :: play 
*		displays hertz then plays hertz
*
*/
void play(){
		
		if (analyzeHertz()){
				activeKnob = true;
				if (!blowerState){
						activeState = false;
						chaserState = false;
						hertzCounter = COUNTER_MAX/2;
						segs.segDisp(displayHertz[currHertz]);//display
				}
		}
		else{
				if (!blowerState){
						activeKnob = false;
						activeState = true;
				}
		}
		if (prevHertz != currHertz || hzChange){
				if(knobInactive()){
						prevHertz = currHertz;//update prevHertz
            hzChange = false;
						playSound();
				}
				checkCleanUp();
		}
}


/*
*
*	FxN :: alarmClockRoutines
*		processes states and polling
*
*
*/
void alarmClockRoutine(){
		for (byte i = 0; i < NUM_CLOCKS; i++){
				if (clocks[i].isSet()){//if clock is set
						if (*(states[i])){//if corresponding state is true
								clocks[i].poll();//poll
						}
						else{
								clocks[i].unSetAlarm();//otherwise;unset alarm
						}
				}
				else if (!clocks[i].isSet()){//if clock is no set
						if (*(states[i])){//if state is true
								clocks[i].setAlarm(timers[i]);//turn on alarm
						}
				}
		}
}

/*
*
*	FxN :: loop
*		loops through a state check routin and a play routine.
*
*/
void loop(){
		alarmClockRoutine();
		play();
}
