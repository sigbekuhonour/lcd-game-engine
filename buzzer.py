from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
BUZZER_PIN_POSITION: int = 0

"""

Accepts a soundtrack filename (without extension) and an array of string

Soundtracks should be formatted as a one-line, whitespace-separated series of notes.

Soundtrack can be paused / stopped if necessary.

We are working with a very limited soundfont - the sound effect will pause the soundtrack, play the effect, then restart it.

"""

class SoundFont:

    def __init__(self, music = 'default', soundEffects: list[str] = []):
        self.buzzer: TonalBuzzer = TonalBuzzer(BUZZER_PIN_POSITION)
        self.currentNoteIndex = 0
        self.soundtrackLine = 0
        self.soundEffects = {}

        for effectName in soundEffects: 
            with open(f"assets/soundeffects/{effectName}.txt") as f:
                notes = f.read().strip().split()
                self.soundEffects[effectName] = { q : notes[q] for q in range(len(notes))}
                f.close()

        with open(f"assets/music/{music}.txt") as f:
            notes = f.read().strip().split()
            self.soundtrackLength = len(notes)
            self.musicNotes = {i: notes[i] for i in range(self.soundtrackLength)}
            f.close()

    # Interrupts the soundtrack, play the sound effect, resume. Sole prop is an effect name.
    def playSoundEffect(self, effectName: str):
        self.buzzer.stop()
        effectNotes: list[str] = self.soundEffects[effectName]
        for i in range(len(effectNotes)):
            self.buzzer.play(Tone(effectNotes[i]))
        self.playMusic()
    
    # Play music, on repeat
    def playMusic(self): 
        while True: # run within engine -> stops when engine stops
            for i in range(self.soundtrackLine, self.soundtrackLength):
                self.buzzer.play(Tone(self.musicNotes[i]))
            self.soundtrackLine = 0 


def test():
    player = SoundFont()

    player.playSoundEffect()







if __name__ == "__main__":
    test()