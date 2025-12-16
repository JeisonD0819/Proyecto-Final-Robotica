import rclpy
from rclpy.node import Node
from phantomx_pincher_interfaces.msg import PoseCommand
import sys, termios, tty
from std_msgs.msg import String
import time
from pincher_control.control_servo import PincherController

# >>> ARDUINO (ADD)
import serial
# <<< ARDUINO (ADD)

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)

        if key == '\x1b':  # empieza una secuencia
            key += sys.stdin.read(2)  # lee los otros 2 caracteres
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return key

class Mover(Node):
    def __init__(self):
        super().__init__('mover')

        self.get_logger().info("Nodo Mover iniciado")

        self.pub = self.create_publisher(PoseCommand, '/pose_command', 10)

        self.subscription = self.create_subscription(
            String,           
            'Bring',     
            self.pose_callback,     
            10                      
        
        )
        #self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)
        self.Movem=PincherController()

        # >>> ARDUINO (ADD)
        self.arduino_port = '/dev/ttyACM0'   # o '/dev/ttyUSB0'
        self.arduino_baud = 9600             # debe coincidir con Serial.begin()
        self.arduino = None
        try:
            self.arduino = serial.Serial(self.arduino_port, self.arduino_baud, timeout=0.1)
            time.sleep(2)
            self.get_logger().info(f"Arduino conectado en {self.arduino_port} @ {self.arduino_baud}")
        except Exception as e:
            self.get_logger().error(f"No pude abrir serial Arduino ({self.arduino_port}): {e}")
        # <<< ARDUINO (ADD)

    # >>> ARDUINO (ADD)
    def activarchupa(self):
        if self.arduino is None:
            self.get_logger().warn("Arduino no inicializado; no envío comando.")
            return
        try:
            self.arduino.write(b'B')  # Arduino hace toggle con b/B
            self.arduino.flush()
            self.get_logger().info("Enviado 'B' al Arduino (toggle chupa)")
        except Exception as e:
            self.get_logger().error(f"Error enviando a Arduino: {e}")
    # <<< ARDUINO (ADD)

    def pose_callback(self,msg):

        self.get_logger().info(f"Recibí: {msg.data}")

        Entrada=msg.data
        tAbiertoAV = 4
        tAbiertoAR = 5
        tAgarrar = 5
        
        if (Entrada=="azul"):

            self.msg_poseCommand(0.162,-0.093,0.062,3.142,-0.055,-0.521)
            time.sleep(tAbiertoAV)
            self.Movem.rd_gripper(1.0)
            time.sleep(1)
            self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)
        
        elif (Entrada=="verde"):
            
            self.msg_poseCommand(0.169,0.078,0.062,3.142,-0.055,0.433)
            time.sleep(tAbiertoAV)
            self.Movem.rd_gripper(1.0)
            time.sleep(1)
            self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)

        elif (Entrada=="home"):
            
            self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)
            
            self.Movem.rd_gripper(1.0)
        
        elif (Entrada=="agarrar"):
            self.Movem.rd_gripper(1.0)
            self.msg_poseCommand(0.085, 0.0, 0.049,3.142,-0.038,0.0)
            #{x: 0.085, y: 0.0, z: 0.049, roll: 3.142, pitch: -0.038, yaw: 0.0
            time.sleep(tAgarrar)
            self.Movem.rd_gripper(0.47)
            time.sleep(1)
            self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)

        elif (Entrada=="rojo"):
            self.msg_poseCommand(-0.008, 0.099, 0.141,3.142,-0.006,1.650)
            #{x: -0.008, y: 0.099, z: 0.141, roll: 3.142, pitch: -0.006, yaw: 1.650
            time.sleep(3)
            self.msg_poseCommand(-0.008, 0.099, 0.050,3.142,-0.005,1.650)
            #"{x: -0.008, y: 0.099, z: 0.050, roll: 3.142, pitch: -0.005, yaw: 1.650
            time.sleep(tAbiertoAR)
            self.Movem.rd_gripper(1.0)
            time.sleep(1)
            self.msg_poseCommand(-0.008, 0.099, 0.141,3.142,-0.006,1.650)
            self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)

        elif (Entrada=="amari"):
            self.msg_poseCommand(-0.008, -0.099, 0.141,3.142,-0.006,-1.650)
            time.sleep(3)
            self.msg_poseCommand(-0.008, -0.099, 0.050,3.142,-0.005,-1.650)
            time.sleep(tAbiertoAR)
            self.Movem.rd_gripper(1.0)
            time.sleep(1)
            self.msg_poseCommand(-0.008, -0.099, 0.141,3.142,-0.006,-1.650)
            self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)

        elif (Entrada=="gripper"):  
            self.Movem.rd_gripper(1.0)
            time.sleep(7)
            self.Movem.rd_gripper(0.5)

        elif (Entrada=="agarrarb"):
            self.msg_poseCommand(0.091, 0.0, 0.098,3.142,0.011,0.0)
            self.activarchupa()
            
            #{{x: 0.091, y: 0.000, z: 0.100, roll: 3.142, pitch: 0.011, yaw: 0.000
            time.sleep(tAgarrar)
            self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)

        elif (Entrada=="verdeb"):
            
            self.msg_poseCommand(0.148,0.085,0.126,3.142,-0.09,0.521)
            #{x: 0.148, y: 0.085, z: 0.126, roll: 3.142, pitch: -0.090, yaw: 0.521
            time.sleep(tAbiertoAV)
            self.activarchupa()
            self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)

        elif (Entrada=="azulb"):
            
            self.msg_poseCommand(0.148,-0.085,0.126,3.142,-0.09,-0.521)
            #{x: 0.148, y: -0.085, z: 0.126, roll: 3.142, pitch: -0.090, yaw: -0.521
            time.sleep(tAbiertoAV)
            self.activarchupa()
            self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)
        
        elif (Entrada=="rojob"):
            self.msg_poseCommand(0.002, 0.012, 0.281,-3.142,-1.511,1.401)
            #{x: 0.002, y: 0.012, z: 0.281, roll: -3.142, pitch: -1.511, yaw: 1.401
            time.sleep(3)
            self.msg_poseCommand(-0.008, 0.099, 0.141,3.142,-0.006,1.650)
            time.sleep(2)
            self.msg_poseCommand(0.001, 0.116, 0.112,3.142,-0.007,1.562)
            #{x: 0.001, y: 0.116, z: 0.112, roll: 3.142, pitch: -0.007, yaw: 1.562
            time.sleep(tAbiertoAV)
            self.activarchupa()
            self.msg_poseCommand(-0.008, 0.099, 0.141,3.142,-0.006,1.650)
            self.msg_poseCommand(0.002, 0.012, 0.281,-3.142,-1.511,1.401)
            self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)

        elif (Entrada=="amarib"):
            self.msg_poseCommand(0.002, -0.012, 0.281,-3.142,-1.511,-1.401)
            #{x: 0.002, y: -0.012, z: 0.281, roll: -3.142, pitch: -1.511, yaw: -1.401
            time.sleep(3)
            self.msg_poseCommand(-0.008, -0.099, 0.141,3.142,-0.006,-1.650)
            time.sleep(2)
            self.msg_poseCommand(0.003, -0.122, 0.111,3.142,-0.001,-1.547)
            #{x: 0.003, y: -0.122, z: 0.111, roll: 3.142, pitch: -0.001, yaw: -1.547
            time.sleep(tAbiertoAV)
            self.activarchupa()
            self.msg_poseCommand(0.002, -0.012, 0.281,-3.142,-1.511,-1.401)
            self.msg_poseCommand(0.1, 0.0, 0.14,3.142,0.0,0.0)

        elif (Entrada=="chupa"):
            self.activarchupa()

    def msg_poseCommand(self,x,y,z,r,p,ya):
        msg = PoseCommand()
        msg.x = x
        msg.y = y
        msg.z = z
        msg.roll = r
        msg.pitch = p
        msg.yaw = ya
        msg.cartesian_path = False

        self.pub.publish(msg)
        self.get_logger().info("enviado")

    def msg_poseCommandX(self,x):
        msg = PoseCommand()
        msg.x = x
        msg.cartesian_path = False

        self.pub.publish(msg)
        self.get_logger().info("enviado")

#0.162, -0.093, 0.062   
# 3.142, -0.055, -0.521   
# 
# 0.169, 0.078, 0.062
# 
# 3.142, -0.055, 0.433 
def main():

    rclpy.init()
    print("Elegir teclado(t) o comunicación por nodo(n)")
    node = Mover()
    
    key = get_key()
    

    if (key=="t"):
        inpx=0.1
        inpy=0.0
        inpz=0.1
        node.Movem.move_to_xyz(inpx,inpy,inpz)
        while True:

            key = get_key()

            if(key=="w"):
                print(inpx)
                inpx=inpx+0.01
                node.Movem.move_to_xyz(inpx,inpy,inpz)
            elif(key=="s"):
                print(inpx)
                inpx=inpx-0.01
                node.Movem.move_to_xyz(inpx,inpy,inpz)
            if(key=="a"):
                print(inpy)
                inpy=inpy+0.01
                node.Movem.move_to_xyz(inpx,inpy,inpz)
            elif(key=="d"):
                print(inpy)
                inpy=inpy-0.01
                node.Movem.move_to_xyz(inpx,inpy,inpz)
            if(key=="q"):
                print(inpz)
                inpz=inpz+0.01
                node.Movem.move_to_xyz(inpx,inpy,inpz)
            elif(key=="e"):
                print(inpz)
                inpz=inpz-0.01
                node.Movem.move_to_xyz(inpx,inpy,inpz)

            # >>> ARDUINO (ADD)
            elif (key=="b") or (key=="B"):
                node.activarchupa()
            # <<< ARDUINO (ADD)

            elif(key=="x"):
                break
            
    elif(key=="n"):
        print("activación comunicación")
        rclpy.spin(node)

    #rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
