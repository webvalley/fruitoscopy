import os
import time

HOME_PATH  = os.path.dirname(os.path.abspath(__file__))

def time_now():
    """
    This function receive as input nothing.
    The return is the current timestamp.

    The purpose of this function is to get the timestamp from the raspberry without asking to any device.
    To do so a sync is needed.

    The timestamp is calculated knowing the difference between the raspberry timestamp and the phone timestamp.
    Fianal timestamp = raspberry_timestamp + difference_in_timestamp

    Specifically:
    @@@@@@@@@@@@@

    :Return values:
    ----------
    - The current timestamp
    """
    in_file = open(HOME_PATH + "/timestamp.txt","r")
    text = in_file.read()
    from_file = int(text)
    time_to_send = int(time.time()) + from_file
    return time_to_send

def update_time(timestamp):
    """
    This function receive as input the current timestamp of the device connected to the raspberry.
    No return is given

    The purpose of this function is to update the file with the difference of the tymestamp between the device and the raspberry
    to get a precise metadata

    Specifically:
    @@@@@@@@@@@@@

    :Values in input:
    ----------
    :value 0: The timestamp of the phone/PC

    :Return values:
    ----------
    - nothing
    """
    out_file = open(HOME_PATH + "/timestamp.txt","w")
    diff_time = int(float(timestamp))-int(time.time())
    out_file.write(str(diff_time))
    out_file.close()
