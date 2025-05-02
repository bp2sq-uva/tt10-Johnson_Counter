# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge


@cocotb.test()
async def test_loopback(dut):
    dut._log.info("Start")

    # Set the clock period to 20 us (50 MHz)
    clock = Clock(dut.clk, 20, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1

    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    str_val = ""

    dut._log.info("Waiting for message.....")

    for i in range(17):
        await RisingEdge(dut.rx_valid)
        str_val = str_val+chr(int(dut.rx_data.value))
        dut._log.info(f"Value so far: {str_val}")
        await FallingEdge(dut.rx_valid)
    assert (str_val == "Hi, I'm Servant!\n"), (
        f"String mismatch: "
        f"Expected 'Hi, I'm Servant!\\n', but got {str_val}. "
    )

@cocotb.test()
async def test_counter(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # ui_in[0] == 1: bidirectional outputs enabled, put a counter on both output and bidirectional pins
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    dut._log.info("Testing counter")
    for i in range(256):
        # assert dut.uo_out.value == dut.uio_out.value
        # assert dut.uo_out.value == i
        await ClockCycles(dut.clk, 1)

    dut._log.info("Testing reset")
    for i in range(5):
        # assert dut.uo_out.value == i
        await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    # assert dut.uo_out.value == 0