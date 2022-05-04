import config
from transitions import Machine
import time
from threading import Thread
import server

class simulador:

    STATESLIST = ['start', 'warming', 'cooling', 'off', 'changing', 'target']

    def __init__(self):
        
        self.temp = config.start_temp
        self.target = config.start_target
        self.temp_max = config.temp_max
        self.temp_min = config.temp_min
        self.target_dist = 0
        self.power = 1
        self.last_target = config.start_target
        self.state = config.start_state
        self.cycle = 0
        self.next_cycle = config.next_cycle

        self.machine = Machine(model=self, states=simulador.STATESLIST, initial ='start')
        self.machine.add_transition(trigger='initialize', source='start', dest='target', after='select_temp_change')
        self.machine.add_transition(trigger='start_cooling', source=['changing', 'target', 'off'], dest='cooling', after='temperature_change_init')
        self.machine.add_transition(trigger='start_warming', source=['changing', 'target', 'off'], dest='warming', after='temperature_change_init')
        self.machine.add_transition(trigger='target_changing', source='*', dest='changing', after='select_temp_change')
        self.machine.add_transition(trigger='target_achieved', source=['warming', 'cooling'], dest='target', after='temperature_change_init')

        self.machine.add_transition(trigger='power_off', source='*', dest='off', after='temperature_change_init')
        self.machine.add_transition(trigger='power_on', source='off', dest='target', after='select_temp_change')
      

    def temperature_change_init(self):
        self.target_dist = abs(self.temp - self.target)
        self.cycle = 0

    def caclulate_temp_change(self):
        if self.cycle < 0 and self.temp < self.target:
            return (self.next_cycle**2.0)
            self.cycle = 0
        return (self.cycle**2.0)

    def select_temp_change(self):
        if self.target < self.temp:
            print('select cooling')
            self.start_cooling()
        elif self.target > self.temp:
            print('select warming')
            self.start_warming()
        self.temperature_change_init()
    

def start_thermostat():
    print('Simulator initialized')
    cycle = 0
    clock = time.time()
    sim = simulador()

    server_thread = Thread(target=server.start_server, args=[sim])
    server_thread.start()
    

    while True:
        # Thermostat is on

        if sim.power == 1:
            #If the machine start working again from off state
            if sim.machine.get_state(sim.state).name == 'off':
                sim.power_on()

            #Initialize the thermostat 
            if sim.machine.get_state(sim.state).name == 'start':
                print("STATE 1 on")
                sim.initialize()

            #Target temperature change
            elif sim.target != sim.last_target:
                sim.target_changing()
                sim.last_target = sim.target
                print('Target changed')

            elif sim.machine.get_state(sim.state).name == 'warming':
                print("STATE 2 warming, Temperature = {}".format(sim.temp))

                if sim.temp > sim.target:
                    sim.target_achieved()
                else:
                    sim.temp += sim.caclulate_temp_change()
                    if sim.temp < sim.target-(sim.target_dist/2):
                        sim.cycle += sim.next_cycle
                    else:
                        sim.cycle -= sim.next_cycle

            elif sim.machine.get_state(sim.state).name == 'cooling':
                print("STATE 3 cooling, Temperature = {}".format(sim.temp))
                if sim.temp < sim.target:
                    sim.target_achieved()
                else:
                    sim.temp -= sim.caclulate_temp_change()
                    if sim.temp > sim.target+(sim.target_dist/2):
                        sim.cycle += sim.next_cycle
                    else:
                        sim.cycle -= sim.next_cycle
            
            elif sim.machine.get_state(sim.state).name == 'target':
                print("STATE 4 target")

        # Thermostat is off
        elif sim.power == 0:
            print("STATE 5 off")
            if sim.machine.get_state(sim.state).name != 'off':
                sim.power_off()
            if sim.temp > config.env_temp:
                sim.temp -= sim.caclulate_temp_change()
                if sim.temp > config.env_temp+(sim.target_dist/2):
                    sim.cycle += sim.next_cycle
                else:
                    sim.cycle -= sim.next_cycle
            else:
                sim.temp += sim.caclulate_temp_change()
                if sim.temp < config.env_temp-(sim.target_dist/2):
                    sim.cycle += sim.next_cycle
                else:
                    sim.cycle -= sim.next_cycle
        
        time.sleep(config.simulation_sleep)

def main():
   start_thermostat()

if __name__ == "__main__":
   main()