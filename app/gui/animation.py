import time
from .spirograph import render_spirograph
import formule
from audio.getter import input_sound_start, input_sound_end

done_recording = False
MAX_TIME_RECORDING = 1000

def input_animation_handler(canvas):
    from random import randint
    global done_recording

    input_sound_start("_")
    n_iter = 0
    while not done_recording and n_iter < MAX_TIME_RECORDING:
        canvas.remove_all()
        if n_iter%2 == 0:
            render_spirograph(
                canvas,
                (-50,0),
                20,
                12,
                randint(7,15),
                randint(4,6),
                50,
                3,
                iter_color = formule.colors_creator.gen_random_color_scheme()
            )
        else:
            render_spirograph(
                canvas,
                (50,0),
                25,
                9,
                randint(9,14),
                randint(4,8),
                50,
                3,
                iter_color = formule.colors_creator.gen_random_color_scheme()
            )


        time.sleep(1)
        n_iter += 1
    
    done_recording = False
    input_sound_end("_")
    canvas.remove_all()

def stop_input_animation(canvas):
    global done_recording
    done_recording = True
    canvas.remove_all()