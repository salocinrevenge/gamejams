"""
PLEASE READ THIS PART...

Code to demonstrate multiprocessing in python using a loading screen
This code is only to demonstrate a simple scenario
For complicated situations involving multiple child processes,
it is recommended to create a queue of such processes to manage them properly

This demo uses pygame to represent the loading screen,
but it can be extended to any graphics library

"""

import multiprocessing
import os
import time
from multiprocessing.connection import Connection
from multiprocessing import Queue
import math

import pygame

pygame.init()


def load_directory_batch(queue: Queue, directory: str, files: list):
    """
    Process a batch of files, convert them to ASCII, and send the results to the queue.
    """
    def image_to_ascii(_img: pygame.Surface):
        size = 10
        chars = "  _.,-=+:;cba|?0123456789$W#@"[::-1]
        font = pygame.font.SysFont('consolas', size)

        _img = pygame.transform.scale_by(_img, 0.25)

        def text(msg):
            return font.render(msg, True, (255, 255, 255))

        def map_to_range(value, from_x, from_y, to_x, to_y):
            return value * (to_y - to_x) / (from_y - from_x)

        w, h = text('a').get_size()
        x = 7
        surf = pygame.Surface(((_img.get_width() - 1) * x + w, (_img.get_height() - 1) * x + h))
        _img.lock()
        for j in range(_img.get_height()):
            for i in range(_img.get_width()):
                r, g, b, _ = _img.get_at([i, j])
                if (r, g, b) == (255, 255, 255):
                    continue
                k = (r + g + b) / 3
                index = round(map_to_range(k, 0, 255, 0, len(chars) - 1))
                t = text(chars[index])
                surf.blit(t, (i * x, j * x))
        _img.unlock()
        return surf

    for file in files:
        img = pygame.image.load(os.path.join(directory, file))
        img = image_to_ascii(img)
        data_to_send = [
            img.get_size(),
            pygame.image.tostring(img, 'RGB')
        ]
        queue.put(data_to_send)
        print(f'Loaded image: {file}')


def loading_screen(queue: Queue, item_c):
    """
    Loads and returns the loaded images while displaying a loading screen.
    All loaded images are retrieved using the queue.
    """
    images = []
    _fps = 60
    _clock = pygame.time.Clock()
    _c = 0
    while True:
        for _e in pygame.event.get():
            if _e.type == pygame.QUIT:
                quit()
            if _e.type == pygame.KEYDOWN:
                if _e.key == pygame.K_ESCAPE:
                    quit()
        if not queue.empty():
            img = queue.get()
            img = pygame.image.fromstring(img[1], img[0], "RGB")
            img.set_colorkey((0, 0, 0))
            images.append(img)
            _c += 1
            if _c >= item_c:
                return images
        screen.fill((0, 0, 55))
        w, h = 1000, 800
        _w = w // (2 * item_c)
        pygame.draw.rect(screen, 'white', (w // 4, h // 2 - 50, w // 2, 100), 5)
        for i in range(_c):
            pygame.draw.rect(screen, 'white', (w // 4 + i * _w, h // 2 - 50, _w, 100))
        pygame.display.update()
        _clock.tick(_fps)


if __name__ == '__main__':
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('Loading Screen with MultiProcessing queue')
    fps = 60
    clock = pygame.time.Clock()

    # Parameters
    num_processes = 4  # Number of parallel processes (parametrizable)
    directory = os.path.abspath('car')
    files = os.listdir(directory)
    files.sort(key=lambda a: int(a.split('.')[0].split('_')[1]))

    # Split files into batches for each process
    batch_size = math.ceil(len(files) / num_processes)
    file_batches = [files[i:i + batch_size] for i in range(0, len(files), batch_size)]

    # Create a queue for communication
    queue = Queue()

    # Start processes
    processes = []
    for batch in file_batches:
        process = multiprocessing.Process(target=load_directory_batch, args=(queue, directory, batch))
        process.start()
        processes.append(process)

    # Load images using the loading screen
    all_images = loading_screen(queue, len(files))

    # Wait for all processes to finish
    for process in processes:
        process.join()

    timer = time.time()
    c = 0

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    quit()
        screen.fill((0, 0, 55))
        if time.time() - timer > 0.1:
            timer = time.time()
            c += 1
            c %= len(all_images)
        image = all_images[c]
        screen.blit(image, image.get_rect(center=(500, 400)))
        pygame.display.update()
        clock.tick(fps)
