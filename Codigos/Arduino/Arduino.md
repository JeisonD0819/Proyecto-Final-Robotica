// Definimos el pin donde conectaremos la señal del relé
const int pinRele = 8; 

// Variable para guardar el estado actual (Encendido/Apagado)
bool estadoRele = false; 

void setup() {
  // Iniciamos la comunicación con el computador
  Serial.begin(9600); 
  
  // Configuramos el pin del relé como salida
  pinMode(pinRele, OUTPUT);
  
  // Nos aseguramos que empiece apagado
  digitalWrite(pinRele, LOW); 
  
  Serial.println("Sistema listo. Presiona 'b' y Enter en el monitor serie.");
}

void loop() {
  // Verificamos si el computador ha enviado algún dato
  if (Serial.available() > 0) {
    
    // Leemos el caracter enviado
    char tecla = Serial.read(); 
    
    // Verificamos si la tecla es 'b' (o 'B' mayúscula por si acaso)
    if (tecla == 'b' || tecla == 'B') {
      
      // Cambiamos el estado (Toggle): De true a false o viceversa
      estadoRele = !estadoRele; 
      
      // Aplicamos el nuevo estado al pin
      digitalWrite(pinRele, estadoRele ? HIGH : LOW);
      
      // Retroalimentación en pantalla
      if(estadoRele){
        Serial.println("Rele ENCENDIDO");
      } else {
        Serial.println("Rele APAGADO");
      }
    }
  }
}
