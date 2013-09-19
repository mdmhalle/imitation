#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    play
    ~~~~

    player that shoots photos for every frame at some interval
"""

import os
import time
import Queue
import subprocess


class TransientViewer(object):
    def __init__(self, filename, showtime):
        self.filename = filename

    # def __enter__(self):
    #     self.process = subprocess.Popen(['feh', self.filename])

    # def __exit__(self, type, value, traceback):
    #     self.process.terminate()


def play_folder(folder, interval):
    filenames = os.listdir(folder)
    filenames.sort()
    filenames = (os.path.join(folder, name) for name in filenames)

    # for filename in filenames:
    #     with TransientViewer(filename):
    #         time.sleep(interval)
    start_time = time.time()
    next_time = start_time + interval
    image_queue = Queue.Queue()
    for filename in filenames:
        image = subprocess.Popen(['feh', filename])
        image_queue.put(image)
        if image_queue.qsize() >= 3:
            old_image = image_queue.get()
            old_image.terminate()
        while time.time() < next_time:
            pass
        next_time += interval
        print image_queue.qsize()
    while not image_queue.empty():
        old_image = image_queue.get()
        old_image.terminate()


if __name__ == '__main__':
    import sys
    try:
        folder, interval = sys.argv[1], int(sys.argv[2])
    except IndexError:
        print 'please provide a folder and shooting interval'
        sys.exit(1)


    play_folder(folder, interval)

    print 'done'
