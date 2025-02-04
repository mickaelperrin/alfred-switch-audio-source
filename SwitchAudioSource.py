from subprocess import check_output, call
from json import dumps, loads
from sys import stdout
from os import environ


PATH_TO_SWITCH_AUDIO_OUTPUT = environ['SWITCH_AUDIO_SOURCE_PATH']
LOOKUP_WARNING = "Error: Could not find SwitchAudioSource"


class AudioSource:
    def __init__(self, description, active):
        audioSourceJSON = loads(description)
        title = audioSourceJSON["name"]
        self.uid = audioSourceJSON["uid"]
        self.arg = audioSourceJSON["id"]
        self.title = title
        self.autocomplete = title
        self.type = audioSourceJSON["type"]

        self.icon = {"path": "icons/active.png" if active ==
                     title else "icons/inactive.png"}

    def __str__(self):
        return str(self.__dict__)


def get_sources():
    active = check_output([
        PATH_TO_SWITCH_AUDIO_OUTPUT, '-c'
    ]).strip()

    command_output = check_output([
        PATH_TO_SWITCH_AUDIO_OUTPUT, '-a', '-t', 'output', '-f', 'json'
    ])

    return map(lambda line: AudioSource(line, active), command_output.splitlines())


def get_current():
    command_output = check_output([
        PATH_TO_SWITCH_AUDIO_OUTPUT, '-c'
    ]).replace("\n", "")
    stdout.write(command_output)


def set_output(device):
    check_output([
        PATH_TO_SWITCH_AUDIO_OUTPUT, '-i', device
    ])
    stdout.write(device)


def no_path_provided():
    stdout.write(dumps({
        "items": [{
            "title": LOOKUP_WARNING
        }]
    }))
    exit()
