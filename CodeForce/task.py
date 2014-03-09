import settings
import sys

sys.stdin = open(r'{tournament}\Tests\test{task}_{test}'.format(tournament=settings.Tournament, task=settings.Task,
                                                                test=settings.Test))
__import__('{tournament}.task{task}'.format(tournament=settings.Tournament, task=settings.Task))