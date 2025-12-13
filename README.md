# Proyecto final de robotica 2025-2
Proyecto final de Robótica 2025-2s

# Integrantes
1. Jeison Nicolás Diaz Arciniegas [jediazar@unal.co](JeisonD0819)
2.  [mramoscu@unal.edu.co](MateoKGR)
3.
4

# Informe

Indice:
1. [Objetivos](#objetivos)
2. [Procedimientos realizados](#procedimientos_realizados)
3. [Funcionamiento general y decisiones de diseño](#funcionamiento_y_diseño)
4. [Diagrama de flujo](#diagrama_de_flujo)
5. [Análisis y conclusiones](#conclusiones)


## Objetivos

- Familiarizarse con la arquitectura de ROS2 (nodos, tópicos, mensajes y servicios).
- Implementar un nodo en Python capaz de publicar mensajes del tipo `Twist` para controlar el simulador *turtlesim*.
- Utilizar el servicio `/reset` de turtlesim para reiniciar la posición y orientación de la tortuga.
- Desarrollar un sistema de lectura de teclado en tiempo real que permita el control manual de la tortuga (flechas) y la ejecución de trayectorias predefinidas para dibujar letras.
- Consolidar en un mismo programa la interacción entre tópicos, servicios y entrada del usuario.

## Procedimientos realizados



## Diagrama de flujo

```
## Análisis y conclusiones

A lo largo del desarrollo de este laboratorio logramos comprender de manera práctica cómo se estructura y se ejecuta un nodo en ROS2, y cómo se integran en un mismo programa distintas herramientas como tópicos, servicios y lectura de dispositivos externos (en este caso, el teclado). El análisis del comportamiento del código y del funcionamiento del sistema nos permitió identificar cuáles son los elementos esenciales para controlar un robot sencillo dentro de un entorno simulado.

En primer lugar, el uso del tópico `/turtle1/cmd_vel` para enviar mensajes `Twist` nos enseñó la importancia de entender el flujo de información en ROS2. La tortuga únicamente se mueve si recibe un mensaje bien estructurado, y esto nos obligó a comprender la naturaleza de los campos lineales y angulares, además del rol del *publisher* como interfaz de salida del nodo. A nivel práctico, comprobamos que controlar un robot muchas veces se reduce a modificar correctamente estas velocidades.

El uso del servicio `/reset` fue otra parte fundamental del análisis. Al integrarlo dentro del flujo del programa, aprendimos cómo funciona la comunicación cliente-servidor en ROS2 y cómo se deben construir las *requests* cuando un servicio no requiere datos adicionales. También observamos que trabajar con servicios nos permite modificar estados del sistema que no dependen directamente de la lectura o publicación en tópicos, como en este caso, reiniciar la pose de la tortuga. Esta separación funcional —tópicos para acciones continuas, servicios para acciones puntuales— es un concepto central en las arquitecturas robóticas modernas.

Desde el punto de vista del diseño del programa, la decisión de leer el teclado directamente de la terminal nos permitió crear un sistema de control interactivo, casi en tiempo real, que imita el comportamiento de un teleoperador sencillo. Este proceso nos obligó a entender cómo capturar entradas sin bloqueo, cómo interpretar secuencias de escape y cómo adaptar esas entradas a comandos válidos para *turtlesim*. El análisis de esta parte del código evidencia la importancia de considerar siempre cómo se comunica el usuario con el robot.

Otro aspecto relevante fue la creación de funciones independientes para dibujar cada letra. Aunque se podría haber optado por un diseño más complejo o generalizable, este enfoque nos permitió centrarnos en el control por velocidad y tiempo, entendiendo de manera intuitiva la relación entre estos parámetros y el desplazamiento final del robot. El análisis de estas rutinas reveló que, incluso en sistemas simples, lograr un movimiento preciso requiere iteración, ajuste fino y comprensión de la dinámica del simulador.

Finalmente, la integración de todo el programa en un bucle principal evidenció la importancia de tener un flujo de ejecución ordenado y fácil de seguir. Este bucle centralizó la interacción con el usuario, la captura de teclado, la selección de rutinas y la salida del programa, demostrando que una buena organización del código facilita tanto su mantenimiento como su funcionalidad.

En conclusión, este laboratorio no solo permitió controlar la tortuga de *turtlesim*, sino que nos brindó un entendimiento más profundo de la arquitectura de ROS2, la comunicación entre nodos, el uso de servicios, la importancia de los tópicos y las decisiones prácticas que se deben tomar al diseñar un sistema de control robótico. El resultado final refleja un equilibrio entre simplicidad, funcionalidad y aprendizaje significativo, preparándonos para manejar sistemas más complejos en futuras prácticas.



