/*
  Web client
 
 This sketch connects to a website (http://www.google.com)
 using an Arduino Wiznet Ethernet shield. 
 
 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 
 created 18 Dec 2009
 by David A. Mellis
 modified 9 Apr 2012
 by Tom Igoe, based on work by Adrian McEwen
 
 */

#include <SPI.h>
#include <Ethernet.h>

// Enter a MAC address for your controller below.
// Newer Ethernet shields have a MAC address printed on a sticker on the shield
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
//IPAddress server(173,194,71,139);  // numeric IP for Google (no DNS)
char server[] = "soda.martinfredriksson.com";    // name address for Google (using DNS)
//char server[] = "google.com";
// Set the static IP address to use if the DHCP fails to assign
IPAddress ip(10,42,0,2);

// Initialize the Ethernet client library
// with the IP address and port of the server 
// that you want to connect to (port 80 is default for HTTP):
EthernetClient client;

void setup() {
  
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // no point in carrying on, so do nothing forevermore:
    // try to congifure using IP address instead of DHCP:*/
    Ethernet.begin(mac, ip);
  }
  // give the Ethernet shield a second to initialize:
  delay(1000);
    Serial.print(Ethernet.localIP());
    Serial.print(", " );
    Serial.print(Ethernet.subnetMask() );
    Serial.print(", " );
    Serial.print(Ethernet.gatewayIP() );
    Serial.print(", " );
    Serial.println(Ethernet.dnsServerIP() );
/*
  // if you get a connection, report back via serial:
  if (client.connect(server, 80)) {
    Serial.println("connected");
    // Make a HTTP request:
    client.println("GET /gen.php HTTP/1.1");
    client.println("Host: soda.martinfredriksson.com");
    client.println("Connection: close");
    client.println();
  } 
  else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  } */
  
  // make the pins outputs:
  pinMode(5, OUTPUT); 
  pinMode(6, OUTPUT); 
  pinMode(7, OUTPUT); 
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);  
}

void loop()
{
  
  
  // if there are incoming bytes available 
  // from the server, read them and print them:
  if (client.available()) {
    String s = "";
    char c = ' ';
    int i = 0;
    do {
      c = client.read();
      s.concat(c);
      i++;
    } while (c != '}' || i > 1000);
    client.stop();
    Serial.println(s);
    if (i<1000) {
      int i = s.indexOf("{");
      if (i != -1) {
        dispense(s[i+14]);
      } else {
        Serial.println("Finns inte json :( ");
      }
     }  else Serial.println("TOO MANY LOOPS!");
  }

  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
    
    Serial.println("connecting...");
    // if you get a connection, report back via serial:
    if (client.connect(server, 80)) {
      Serial.println("connected");
      // Make a HTTP request:
      client.println("GET /gen.php HTTP/1.1");
      client.println("Host: soda.martinfredriksson.com");
      client.println("Connection: close");
      client.println();
    } 
    else {
      // kf you didn't get a connection to the server:
      Serial.println("connection failed");
    }
  }
  Serial.print('.');
  
}
void dispense(char a) {
    switch(a) {
      case '1': dispense(1); break;
      case '2': dispense(2); break;
      case '3': dispense(3); break;
      case '4': dispense(4); break;
      case '5': dispense(5); break;
      default: break;
    }
}
void dispense(int num) {
  digitalWrite(10-num, HIGH);
  delay(1000);
  digitalWrite(10-num, LOW);
  delay(5000);
}

