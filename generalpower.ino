#define PIN_FOTORES A5
#define PIN_LED 13

bool lettura;

void setup()
{
	Serial.begin(9600);
	pinMode(PIN_FOTORES, INPUT);
}

void loop()
{
	//Serial.println(analogRead(PIN_FOTORES));
	
	if(analogRead(PIN_FOTORES)>500)
	{
		if(lettura==0)
		{
			lettura=1;
			Serial.println("b");
			digitalWrite(PIN_LED,1);
		}
	}
	else
	{
		lettura=0;
		digitalWrite(PIN_LED,0);
	}
}