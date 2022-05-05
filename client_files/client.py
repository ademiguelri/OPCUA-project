from opcua import Client, ua
import time
import psycopg2

URL = "opc.tcp://127.0.0.1:4840"
CONNECTION = "postgres://postgres:password@localhost:5432/thermostat"

global temp_val
global state_val
global target_val
global power_val

class DataHandler(object):
   def datachange_notification(self, node, val, data):
      if str(node) == 'ns=2;s=V1.Temperature':
         global temp_val
         temp_val = val
      elif str(node) == 'ns=2;s=V1.State':
         global state_val
         state_val = val  
      elif str(node) == 'ns=2;s=V1.Target':
         global target_val
         target_val = val  
      elif str(node) == 'ns=2;s=V1.Power':
         global power_val
         power_val = val


def insert_values(temp, state, target, power):
   conn = psycopg2.connect(CONNECTION)
   cursor = conn.cursor()
   cursor.execute("INSERT INTO therm1 (datetime, temp, state, target, power) VALUES (current_timestamp,"+str(temp)+",'"+str(state)+"',"+str(target)+","+str(power)+")")
   conn.commit()
   cursor.close()
   print()


client = Client(URL)

client.connect()
print("Client connected")

temp = client.get_node('ns=2;s=V1.Temperature')
state = client.get_node('ns=2;s=V1.State')
target = client.get_node('ns=2;s=V1.Target')
power = client.get_node('ns=2;s=V1.Power')
max = client.get_node('ns=2;s=V1.Max_temp')
min = client.get_node('ns=2;s=V1.Min_temp')

temp_val = temp.get_value()
state_val = state.get_value()
target_val = target.get_value()
power_val = power.get_value()

handler_temp = DataHandler()
sub_data = client.create_subscription(500, handler_temp)
handle_data = sub_data.subscribe_data_change(temp)
handle_data = sub_data.subscribe_data_change(state)
handle_data = sub_data.subscribe_data_change(target)
handle_data = sub_data.subscribe_data_change(power)

while True:
   insert_values(temp_val, state_val, target_val, power_val)
   time.sleep(5)
