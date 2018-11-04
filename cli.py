import cmd


def add_note_type(cls, abbreviation, note_type):
    def inner_add_note_type(self, arg):
        self._noter.add_note(note_type, arg)

    inner_add_note_type.__doc__ = "docstring for method %s" % note_type
    inner_add_note_type.__name__ = "do_%s" % abbreviation
    setattr(cls, inner_add_note_type.__name__, inner_add_note_type)


class CLI(cmd.Cmd):
    intro = 'Type help or ? to list commands.\n'
    prompt = '(ntr) '

    def __init__(self, noter):
        super().__init__()
        self._noter = noter
        self.prompt = self.create_prompt()

    def do_list(self, arg):
        """list all notes so far, latest n notes, or all notes of a specific type"""
        if arg != '':
            try:
                notes = self._noter.n_latest_notes(int(arg))
            except ValueError:
                notes = self._noter.all_notes_of_type(arg)
        else:
            notes = self._noter.all_notes()

        self._print_notes(notes)

    def do_capt(self, arg):
        """take screenshot"""
        self._noter.take_screenshot()

    def do_exit(self, arg):
        """exit"""
        self._noter.add_note('end', None)
        return True

    @staticmethod
    def _print_notes(notes):
        for note in notes:
            print(
                '{} - {:18s} {}'.format(note['timestamp'].strftime('%Y-%m-%dT%H:%M:%S'), note['type'], note['content']))

    def create_prompt(self):
        elapsed_seconds = self._noter.calculate_elapsed_seconds()
        elapsed_percentage = elapsed_seconds / (self._noter._duration * 60)

        return '(ntr {:.0f}/{:d} {:.1%}) '.format(elapsed_seconds / 60, self._noter._duration, elapsed_percentage)

    def postcmd(self, stop, line):
        self.prompt = self.create_prompt()

        return stop
