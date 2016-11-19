from subprocess import call


class NanoTts(object):
    VOICES = [ "en-GB", "en-US", "de-DE", "es-ES", "fr-FR", "it-IT" ]

    def __init__(self):
        self.voice = "en-GB"
        self.noplay = False
        self.output = None
        self.speed = None

    @staticmethod
    def get_voices():
        """
        Returns available voices.
        """
        return NanoTts.VOICES

    def run(self, words):
        command_list = ["nanotts", ]
        if self.voice:
            command_list.extend(["-v", self.voice])
        if self.noplay:
            command_list.append("--no-play")
        if self.output:
            command_list.extend(["-o", self.output])
        if self.speed:
            command_list.extend(["--speed", str(self.speed)])
        command_list.extend(["-w", words])
        call(command_list)
