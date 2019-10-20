# we assume the raspberry_pi ip address is 192.168.43.7
# In the compurter that you run a simulator, run this command: (out=udp:the_ip_of_computer_where_you_run_your_mavsdk_python_script)
mavproxy.py --master=udp:127.0.0.1:14540 --master=udp:127.0.0.1:14550 --master=udp:127.0.0.1:14560 --out=udp:192.168.43.8:14540 --out=udp:192.168.43.8:14550 --out=udp:192.168.43.8:14560


# In the raspberry_pi, you run the code with:
#await drone.connect(system_address="udp://:14540")
