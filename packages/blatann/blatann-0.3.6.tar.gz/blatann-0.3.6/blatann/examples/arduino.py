from blatann import BleDevice
from blatann.gap import smp, AdvertisingData
from blatann.examples import example_utils, constants
from blatann.gatt.gatts import GattsCharacteristicProperties
from blatann.nrf import nrf_events
from blatann.services import device_info, battery

logger = example_utils.setup_logger(level="DEBUG")


def setup_peripheral(serial_port):
    # Create and open the BLE device (and suppress spammy logs)
    ble_device = BleDevice(serial_port)
    ble_device.event_logger.suppress(nrf_events.GapEvtAdvReport)
    ble_device.open()

    adv_data = AdvertisingData(local_name="ArduinoTest")
    ble_device.advertiser.set_advertise_data(adv_data)

    dis = device_info.add_device_info_service(ble_device.database)
    battery.add_battery_service(ble_device.database, enable_notifications=True)
    service_uuid = constants.DESC_EXAMPLE_SERVICE_UUID
    char_uuid = constants.DESC_EXAMPLE_CHAR_UUID
    svc = ble_device.database.add_service(service_uuid)
    svc.add_characteristic(char_uuid, GattsCharacteristicProperties(read=True, notify=True))

    ble_device.advertiser.start(150)
    return ble_device


def main(serial_port, use_periph=False):
    # Set the target to the peripheral's advertised name
    target_device_name = "ArduinoTest"

    # Create and open the BLE device (and suppress spammy logs)
    ble_device = BleDevice(serial_port)
    ble_device.event_logger.suppress(nrf_events.GapEvtAdvReport)
    ble_device.open()

    if use_periph:
        other_device = setup_peripheral("COM13")
    else:
        other_device = None

    target_address = example_utils.find_target_device(ble_device, target_device_name)
    if not target_address:
        logger.info("Did not find target peripheral")
        return

    # Initiate the connection and wait for it to finish
    logger.info("Found match: connecting to address {}".format(target_address))
    peer = ble_device.connect(target_address).wait()
    if not peer:
        logger.warning("Timed out connecting to device")
        ble_device.close()
        return

    logger.info("Connected, conn_handle: {}".format(peer.conn_handle))
    _, event_args = peer.discover_services().wait(30)
    logger.info(f"Database: {peer.database}")

    peer.disconnect().wait()
    ble_device.close()
    if use_periph:
        other_device.close()


if __name__ == '__main__':
    main("COM11")
