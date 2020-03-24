import os
import datetime


class PrintMessage:
    TIME_MAXWIDTH = 26
    OPCODE_MAXWIDTH = 16
    DESCRIPTION_MAXWIDTH = 40
    ERROR_MAXWIDTH = 20
    ERROR_SYMBOL = "#"
    FILENAME = ""
    DIR_SORT_LOG = "sorting_logs"
    DIR_UNSORT_LOG = "unsorting_logs"
    flag_table_header = False

    def __init__(self):
        self.FILENAME = datetime.datetime.now().strftime('%d.%m.%Y_%H-%M-%S') + ".log"
        if os.path.isdir(self.DIR_SORT_LOG) is False:
            os.makedirs(self.DIR_SORT_LOG)
        with open(self.DIR_SORT_LOG + "/S_" + self.FILENAME, "w"):
            pass
        if os.path.isdir(self.DIR_UNSORT_LOG) is False:
            os.makedirs(self.DIR_UNSORT_LOG)
        with open(self.DIR_UNSORT_LOG + "/U_" + self.FILENAME, "w"):
            pass

    @staticmethod
    def __time_now():
        return datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S.%f')

    def __divider_str(self, message):
        lines = list()
        lines.append("")
        count_lines = 0
        for word in message.split():
            if len(word) > self.DESCRIPTION_MAXWIDTH:
                word = word[:self.DESCRIPTION_MAXWIDTH - 3] + "..."
            if len(lines[count_lines] + word) > self.DESCRIPTION_MAXWIDTH:
                lines[count_lines] = lines[count_lines][:-1]
                count_lines += 1
                lines.append("")
            lines[count_lines] += word + " "
        lines[count_lines] = lines[count_lines][:-1]

        return lines

    def __write_in_sort_file(self, message):
        with open(self.DIR_SORT_LOG + "/S_" + self.FILENAME, "a") as file:
            file.write(message + "\n")

    def __write_in_unsort_file(self, message):
        with open(self.DIR_UNSORT_LOG + "/U_" + self.FILENAME, "a") as file:
            file.write("{0:s} {1:s}\n".format(self.__time_now(), message))

    def __print_border(self):
        msg = "+{0:^{w_time}s}+{1:^{w_opcode}s}+{2:^{w_description}s}+{3:^{w_error}s}+".format(
            "-" * (self.TIME_MAXWIDTH + 2),
            "-" * (self.OPCODE_MAXWIDTH + 2),
            "-" * (self.DESCRIPTION_MAXWIDTH + 2),
            "-" * (self.ERROR_MAXWIDTH + 2),
            w_time=self.TIME_MAXWIDTH+2,
            w_opcode=self.OPCODE_MAXWIDTH+2,
            w_description=self.DESCRIPTION_MAXWIDTH+2,
            w_error=self.ERROR_MAXWIDTH+2)

        # print(msg)
        self.__write_in_sort_file(msg)

    def __print_header(self):
        if self.flag_table_header is False:
            self.__print_border()
            msg = "| {0:^{w_time}s} | {1:^{w_opcode}s} | {2:^{w_description}s} | {3:^{w_error}s} |".format(
                "Time",
                "Opcode",
                "Description",
                "Error flag",
                w_time=self.TIME_MAXWIDTH,
                w_opcode=self.OPCODE_MAXWIDTH,
                w_description=self.DESCRIPTION_MAXWIDTH,
                w_error=self.ERROR_MAXWIDTH)
            # print(msg)
            self.__write_in_sort_file(msg)
            self.__print_border()
            self.flag_table_header = True

    def __print_msg(self, opcode, description, error):
        msg = "| {0:^{w_time}s} | {1:^{w_opcode}s} | {2:<{w_description}s} | {3:^{w_error}s} |".format(
            self.__time_now(),
            opcode,
            description,
            error,
            w_time=self.TIME_MAXWIDTH,
            w_opcode=self.OPCODE_MAXWIDTH,
            w_description=self.DESCRIPTION_MAXWIDTH,
            w_error=self.ERROR_MAXWIDTH)

        # print(msg)
        self.__write_in_sort_file(msg)
        self.__write_in_unsort_file(opcode)

    def info(self, opcode, message):
        opc = opcode
        msg = self.__divider_str(message)
        self.__print_header()

        for line in msg:
            self.__print_msg(opc, line, "")
            opc = ""

    def error(self, opcode, message):
        opc = opcode
        msg = self.__divider_str(message)
        self.__print_header()

        for line in msg:
            self.__print_msg(opc, line, self.ERROR_SYMBOL * self.ERROR_MAXWIDTH)
            opc = ""
