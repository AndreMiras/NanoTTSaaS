from subprocess import call


class NanoTts(object):

    def __init__(self):
        self.voice = "en-GB"
        self.noplay = False
        self.output = None

    def run(self, words):
        command_list = ["nanotts", ]
        if self.voice:
            command_list.extend(["-v", self.voice])
        if self.noplay:
            command_list.append("--no-play")
        if self.output:
            command_list.extend(["-o", self.output])
        command_list.extend(["-w", words])
        call(command_list)
