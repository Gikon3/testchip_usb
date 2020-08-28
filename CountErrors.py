class CountErrors:
    MEMORY0 = "DICE_band_cutWell (CGDICE)"
    MEMORY1 = "DICE_band_cutWell (CKLNQD1)"
    MEMORY2 = "DFF (without DICE)"
    MEMORY3 = "DFF (with Hamming)"
    MEMORY4 = "DICE_band_cutWell"
    MEMORY5 = "Hamming code"
    MEMORY6 = "DICE_band"
    MEMORY7 = "DICE_cutWell"
    MEMORY8 = "DICE"
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
                    MEMORY8: 0}

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
