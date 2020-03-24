import datetime
import time
import curses
import ComPort
import PrintMessage
import CountErrors

PORTNAME = "COM11"
THRESHOLD_ERRORS = 64

STM_BUFFER_FILL = "FFDA0F00"
STM_MACHINE = "FFDA0F01"
STM_TIMEOUT_SPI = "FFDA0F02"
STM_EVENT_REG = "FFDA0E00"
STM_SH_UNRESET = "FFDA0A00"

SH_START = "F0DA0000"
SH_MEM_0 = "F0DA1000"
SH_MEM_1 = "F0DA1001"
SH_MEM_2 = "F0DA1002"
SH_MEM_3 = "F0DA1003"
SH_MEM_4 = "F0DA1004"
SH_MEM_5 = "F0DA1005"
SH_MEM_6 = "F0DA1006"

print_mes = PrintMessage.PrintMessage()
com_port = ComPort.ComPort(portname=PORTNAME)
errors = CountErrors.CountErrors()

win = curses.initscr()
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
win.addstr(3, 2, "Errors:")
win.addstr(8, 2, "Events:")
win.addstr(26, 2, " -- To Exit, press ESC -- ")

key = 0
number_errors = 0
count_errors = 0
count_package = 0
error_name = ""

f_number_errors = False
f_errors = False
f_number_errors_alu = False


def flags_reset():
    global number_errors
    global count_errors
    global error_name
    global f_number_errors
    global f_errors
    global f_number_errors_alu

    number_errors = 0
    count_errors = 0
    error_name = ""
    f_number_errors = False
    f_errors = False
    f_number_errors_alu = False


start_time = time.time()
try:
    while key != 27:
        key = win.getch()

        win.addstr(1, 2, datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        win.addstr(1, 24, "{0:.0f} seconds".format(time.time() - start_time))

        i = 4
        for name, value in errors.errors_count.items():
            win.addstr(i, 4, "{0:<8s} {1:<4d}".format(name, value))
            i += 1

        i = 13
        for name, value in errors.events_count.items():
            win.addstr(i, 4, "{0:<15s} {1:<4d}".format(name, value))
            i += 1

        win.addstr(19, 2, "{0:<17s} {1:<4d}".format("Packages", count_package))

        data = com_port.read()

        # print(data)

        if data == SH_START:
            print_mes.info(data, "Start cxemai6")
            errors.event_inc(errors.SH_START)
            flags_reset()

        elif data == STM_BUFFER_FILL:
            print_mes.error(data, "Buffer STM32 fill")
            errors.event_inc(errors.BUFFER_FILL)
            flags_reset()

        elif data == STM_MACHINE:
            print_mes.error(data, "STM automatic break")
            errors.event_inc(errors.MACHINE)
            flags_reset()

        elif data == STM_TIMEOUT_SPI:
            print_mes.error(data, "Timeout SPI")
            errors.event_inc(errors.TIMEOUT_SPI)
            flags_reset()

        elif data == STM_SH_UNRESET:
            print_mes.error(data, "Unreset cxemai6")
            errors.event_inc(errors.UNRESET_DEVICE)
            flags_reset()

        elif data == STM_EVENT_REG:
            print_mes.error(data, "Event shift register")
            errors.error_inc(errors.SHIFT_REG, 1)

        elif data == SH_MEM_0:
            print_mes.info(data, "Memory 0")
            f_number_errors = True
            error_name = errors.MEMORY0

        elif data == SH_MEM_1:
            print_mes.info(data, "Memory 1")
            f_number_errors = True
            error_name = errors.MEMORY1

        elif data == SH_MEM_2:
            print_mes.info(data, "Memory 2")
            f_number_errors = True
            error_name = errors.MEMORY2

        elif data == SH_MEM_3:
            print_mes.info(data, "Memory 3")
            f_number_errors = True
            error_name = errors.MEMORY3

        elif data == SH_MEM_4:
            print_mes.info(data, "Memory 4")
            f_number_errors = True
            error_name = errors.MEMORY4

        elif data == SH_MEM_5:
            print_mes.info(data, "Memory 5")
            f_number_errors = True
            error_name = errors.MEMORY5

        elif data == SH_MEM_6:
            print_mes.info(data, "Memory 6")
            f_number_errors = True
            error_name = errors.MEMORY6

        elif f_number_errors is True:
            f_number_errors = False
            count_package += 1
            errors.error_inc(error_name, int(data, 16))
            if int(data, 16) == 0:
                print_mes.info(data, "Number errors: 0")
            else:
                print_mes.error(data, "Number errors: {0:d}".format(int(data, 16)))
                if f_number_errors_alu is False:
                    number_errors = int(data, 16) * 2 if int(data, 16) < THRESHOLD_ERRORS else THRESHOLD_ERRORS * 2
                else:
                    number_errors = 1
                f_errors = True
            f_number_errors_alu = False

        elif f_errors is True:
            print_mes.error(data, "Error")
            count_errors += 1
            if count_errors == number_errors:
                count_errors = 0
                f_errors = False

        else:
            print_mes.error(data, "Invalid OPCODE")
            errors.event_inc(errors.INVALID_OPCODE)

finally:
    curses.endwin()
