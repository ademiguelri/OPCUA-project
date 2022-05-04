from opcua import Server,ua 
import time

id = 'ns=2;s=V'
id1 = 'ns=2;s=V1'
URL = "opc.tcp://0.0.0.0:4840"

def start_server(object):

    server = Server()
    server.set_endpoint(URL)

    server.set_security_policy([
        ua.SecurityPolicyType.NoSecurity,
        # ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
        # ua.SecurityPolicyType.Basic256Sha256_Sign,
    ])

    node =  server.get_objects_node()
    custom_obj_type = node.add_object_type(id, "Thermostat")

    temp = custom_obj_type.add_variable(0, "Temperature", 0.0)
    temp.set_modelling_rule(True)
    target = custom_obj_type.add_variable(1, "Target", 0.0)
    target.set_modelling_rule(True)
    target.set_writable()
    state = custom_obj_type.add_variable(2, "State", 0.0)
    state.set_modelling_rule(True)
    power = custom_obj_type.add_variable(3, "Power", 0.0)
    power.set_modelling_rule(True)
    power.set_writable()
    max_temp = custom_obj_type.add_variable(4, "Max_temp", 0.0)
    max_temp.set_modelling_rule(True)
    min_temp = custom_obj_type.add_variable(5, "Min_temp", 0.0)
    min_temp.set_modelling_rule(True)

    myobj = node.add_object(id1, "Therm", custom_obj_type.nodeid)

    my_temp = myobj.get_child(["0:Temperature"])
    my_target = myobj.get_child(["1:Target"])
    my_state = myobj.get_child(["2:State"])
    my_power = myobj.get_child(["3:Power"])
    my_max_temp = myobj.get_child(["4:Max_temp"])
    my_min_temp = myobj.get_child(["5:Min_temp"])

    try:
        server.start()
        print('Server connected in {}'.format(URL))

    except:
        print('Error starting the server')
    else:
        target_change = object.target
        power_change = object.power
        my_target.set_value(target_change)
        my_power.set_value(power_change)

        while True:
            my_temp.set_value(object.temp)
            my_state.set_value(object.state)
            my_max_temp.set_value(object.temp_max)
            my_min_temp.set_value(object.temp_min)

            if my_target.get_value() != target_change:
                target_change = my_target.get_value()
                my_target.set_value(target_change)
                object.target = target_change

            if my_power.get_value() != power_change:
                power_change = my_power.get_value()
                my_power.set_value(power_change)
                object.power = power_change

            time.sleep(1)
