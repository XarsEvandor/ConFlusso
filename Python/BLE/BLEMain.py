import asyncio

from matplotlib import pyplot as plt

from CDevice import Device


async def main(device_name_pattern):
    
    SERVICE_UUID = "477fcf1c-b91c-4c23-9004-95211c661945"
    CHAR_UUID = "eebf853b-a580-424c-a827-d6600f4253e1"
    
    device = await Device.create(device_name_pattern, [SERVICE_UUID], [CHAR_UUID])
    
    if device is None:
        print("Failed to connect to device")
        return

    await asyncio.sleep(30) # Collect data for 30 seconds

    await device.services[0].characteristics[0].stop_notify()
    await device.disconnect()
    print("Disconnected.")

    # Plot the collected data
    fig, axs = plt.subplots(2, 3)

    for i, (axis, data) in enumerate(device.services[0].characteristics[0].data.items()):
        timestamps, values = zip(*data)
        row = i // 3
        col = i % 3
        axs[row, col].plot(timestamps, values)
        axs[row, col].set_title(axis)

    for ax in axs.flat:
        ax.set(xlabel='time (ms)', ylabel='value')

    plt.tight_layout()
    plt.show()
    
device_name_pattern = "Arduino Acceleromet" # Regex pattern for the Arduino's name
loop = asyncio.get_event_loop()
loop.run_until_complete(main(device_name_pattern))