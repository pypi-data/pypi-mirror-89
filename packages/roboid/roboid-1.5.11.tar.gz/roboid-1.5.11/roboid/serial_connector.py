# Part of the ROBOID project - http://hamster.school
# Copyright (C) 2016 Kwang-Hyun Park (akaii@kw.ac.kr)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import sys
from timeit import default_timer as timer

import serial.tools.list_ports

from roboid.connector import State
from roboid.connector import Result


BAUD_RATE = 115200
VALID_PACKET_LENGTH = 54
RETRY = 10
TIMEOUT = 0.1


class SerialConnector(object):
    def __init__(self, tag, connection_checker, loader=None):
        self._tag = tag
        self._connection_checker = connection_checker
        self._loader = loader
        self._serial = None
        self._address = "000000000000"
        self._port_name = ""
        self._found = False
        self._timestamp = 0
        self._connected = False

    def open(self, port_name=None):
        if port_name:
            result = self._open_port(port_name)
            if result != Result.NOT_AVAILABLE:
                return result
        else:
            ports = serial.tools.list_ports.comports()
            for port in ports:
                result = self._open_port(port[0])
                if result != Result.NOT_AVAILABLE:
                    return result
        self._print_error("No available USB to BLE bridge")
        return Result.NOT_AVAILABLE

    def _open_port(self, port_name):
        if port_name:
            try:
                s = serial.Serial(port_name, BAUD_RATE, rtscts=True, timeout=0.1)
                s.reset_input_buffer()
                s.reset_output_buffer()
                self._port_name = port_name
                result = self._check_port(s)
                if result != Result.NOT_AVAILABLE:
                    self._serial = s
                    return result
                s.close()
            except:
                pass
        return Result.NOT_AVAILABLE

    def close(self):
        self._connected = False
        if self._serial:
            self._serial.close()
            self._serial = None
        self._print_message("Disposed")

    def is_connected(self):
        return self._connected

    def get_address(self):
        return self._address

    def _set_address(self, address):
        self._address = address

    def _set_connection_state(self, state):
        self._connected = (state == State.CONNECTED)
        if self._found == False and self._connected:
            self._found = True
        if self._found:
            if state == State.CONNECTED:
                address = self._address
                if len(address) >= 12:
                    self._print_message("Connected: {} {}:{}:{}:{}:{}:{}".format(self._port_name, address[10:12], address[8:10], address[6:8], address[4:6], address[2:4], address[0:2]))
                else:
                    self._print_message("Connected: {}".format(self._port_name))
            elif state == State.CONNECTION_LOST:
                self._print_error("Connection lost")

    def _read_line(self, serial):
        try:
            line = bytearray()
            terminator = ord("\r")
            while True:
                c = serial.read()[0]
                line.append(c)
                if c == terminator: break
            return line.decode("utf-8")
        except:
            return ""

    def _read_packet(self, serial, start_byte=None):
        try:
            packet = self._read_line(serial)
            if start_byte is None:
                return packet
            if packet[:2] == start_byte:
                return packet
            return None
        except:
            return None

    def write(self, packet):
        if self._serial:
            try:
                self._serial.write(packet.encode())
            except:
                pass

    def read(self):
        if self._serial:
            try:
                packet = self._read_line(self._serial)
                if len(packet) == VALID_PACKET_LENGTH:
                    if self._found == False:
                        self._check_connection(self._serial)
                    elif self._connected == False:
                        self._set_address(packet[41:53])
                        self._set_connection_state(State.CONNECTED)
                    self._timestamp = 0
                    return packet
                elif self._connected:
                    t = timer()
                    if self._timestamp == 0:
                        self._timestamp = t
                    elif t - self._timestamp > TIMEOUT:
                        self._set_connection_state(State.CONNECTION_LOST)
            except:
                if self._connected:
                    self._set_connection_state(State.CONNECTION_LOST)
        return None

    def _check_port(self, serial):
        self._read_packet(serial)
        packet1 = self._read_packet(serial)
        packet2 = self._read_packet(serial)
        if packet2:
            if len(packet2) == VALID_PACKET_LENGTH:
                return self._check_connection(serial)
            elif packet1 and len(packet2) == 2:
                self._print_error("Not connected")
                return Result.NOT_CONNECTED
        return Result.NOT_AVAILABLE

    def _check_connection(self, serial):
        for i in range(RETRY):
            serial.write("FF\r".encode())
            packet = self._read_packet(serial, "FF")
            if packet:
                packet = packet.strip()
                info = packet.split(",")
                if info and len(info) >= 5:
                    if self._connection_checker.check(info):
                        self._set_address(info[4])
                        if self._loader is not None:
                            self._loader.load(serial, info[4])
                        self._set_connection_state(State.CONNECTED)
                        return Result.FOUND
                return Result.NOT_AVAILABLE
        return Result.NOT_AVAILABLE

    def _print_message(self, message):
        sys.stdout.write("{} {}\n".format(self._tag, message))

    def _print_error(self, message):
        sys.stderr.write("{} {}\n".format(self._tag, message))