class CountErrors:
    MEMORY0 = "Memory0"
    MEMORY1 = "Memory1"
    MEMORY2 = "Memory2"
    MEMORY3 = "Memory3"
    MEMORY4 = "Memory4"
    MEMORY5 = "Memory5"
    MEMORY6 = "Memory6"
    MEMORY7 = "Memory7"
    MEMORY8 = "Memory8"
    SHIFT_REG = "Shift reg"

    SH_START = "cxemai6 start"
    BUFFER_FILL = "Buffer fill"
    UNRESET_DEVICE = "Unreset cxemai6"
    TIMEOUT_SPI = "Timeout SPI"
    MACHINE = "STM automatic break"
    INVALID_OPCODE = "Invalid OPCODE"

    errors_count = {MEMORY0: 0,
                    MEMORY1: 0,
                    MEMORY2: 0,
                    MEMORY3: 0,
                    MEMORY4: 0,
                    MEMORY5: 0,
                    MEMORY6: 0,
                    MEMORY7: 0,
                    MEMORY8: 0,
                    SHIFT_REG: 0}

    events_count = {SH_START: 0,
                    UNRESET_DEVICE: 0,
                    TIMEOUT_SPI: 0,
                    BUFFER_FILL: 0,
                    MACHINE: 0,
                    INVALID_OPCODE: 0}

    def error_inc(self, key, number):
        self.errors_count[key] += number

    def event_inc(self, item):
        self.events_count[item] += 1
