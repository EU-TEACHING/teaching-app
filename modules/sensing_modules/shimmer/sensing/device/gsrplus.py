from xml.dom import NotFoundErr
from serial.tools import list_ports

import sensing.device.shimmer_util as su
from sensing.device.shimmer import Shimmer3


class ShimmerGSRPlus:

    def __init__(self, sampling_rate: int) -> None:
        """Initializes the Shimmer GSR+ sensor device.

        Args:
            sampling_rate (int): the sampling frequency of the sensor
        """        
        self._device = Shimmer3(shimmer_type=su.SHIMMER_GSRplus, debug=True)
        self.sampling_rate = sampling_rate
        
    def stream(self):
        """This generator handles the stream of PPG, EDA and timestamp data from the Shimmer sensor.

        Raises:
            RuntimeError: raised when bluetooth is not connected

        Yields:
            Iterator[Tuple[int, Dict]]: a dictionary with timestamp, PPG and EDA data.
        """        
        if self._device.current_state == su.BT_CONNECTED:
            self._device.start_bt_streaming()
            print("Data streaming started.")
        else:
            raise RuntimeError("Bluetooth is not connected.")
        while True:
            n, packets = self._device.read_data_packet_extended(calibrated=True)
            reads = {'timestamp': [], 'PPG': [], 'EDA': []}
            for pkt in packets:

                timestamp, ppg, eda = pkt[2], pkt[3], pkt[4]

                reads['timestamp'].append(timestamp)
                reads['PPG'].append(ppg)
                reads['EDA'].append(eda)

            yield n, reads
    
    def connect(self, port: str=None) -> bool:
        """This function handles the connection via bluetooth with the Shimmer sensor.

        Args:
            port (str, optional): a string with the device path (e.g., '/dev/ttyUSB0'), 
                otherwise an input from the user is requested. Defaults to None.

        Returns:
            bool: True if  connected successfully.
        """        
        # Selection of the port
        if port is None or port == '':
            raise ValueError("Parameter port cannot be empty or None.")
        
        print(f"Selected {port}")
        
        # Starting connection with the chosen port
        if self._device.connect(com_port=port):
            if not self._device.set_sampling_rate(self.sampling_rate):
                return False
            # After the connection we want to enable GSR and PPG
            if not self._device.set_enabled_sensors(su.SENSOR_GSR, su.SENSOR_INT_EXP_ADC_CH13):
                return False
            # Set the GSR measurement unit to Skin Conductance (micro Siemens)
            if not self._device.set_active_gsr_mu(su.GSR_SKIN_CONDUCTANCE):
                return False
            
            print(f"Shimmer GSR+ connected to {port}.")
            self._device.print_object_properties()
            return True
        
        return False
    
    def disconnect(self) -> bool:
        """Disconnects the Shimmer sensor.

        Returns:
            bool: True if disconnected successfully.
        """        
        if not self._device.current_state == su.BT_CONNECTED:
            self._device.disconnect(reset_obj_to_init=True)
            return True
        else:
            return False
    
