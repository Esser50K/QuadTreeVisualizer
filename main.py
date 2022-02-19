import argparse
import pygame
import random
from quadtree import QuadTree, Rect, Point


def clear(surface: pygame.Surface):
    surface.fill(pygame.Color(0, 0, 35))


def draw_qtree(surface: pygame.Surface, qtree: QuadTree):
    for boundary, points in qtree.get_all():
        pygame.draw.rect(surface, pygame.Color('white'), boundary.to_tuple(), 1)
        for p in points:
            pygame.draw.circle(surface, pygame.Color('white'), p.to_tuple(), 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ASCII Player')
    parser.add_argument("-cw", "--width", type=int, default=800, help="width of the canvas")
    parser.add_argument("-ch", "--height", type=int, default=800, help="height of the canvas")
    parser.add_argument("-qw", "--query-width", type=int, default=50, help="width of the query area")
    parser.add_argument("-qh", "--query-height", type=int, default=50, help="height of the query area")
    parser.add_argument("-rp", "--random-points", type=int, default=0, help="number of prefilled random points")
    args = parser.parse_args()

    width = args.width
    height = args.height
    query_width = args.query_width
    query_height = args.query_height

    # init pygame and canvas
    pygame.init()
    surface = pygame.display.set_mode((width, height))
    clear(surface)

    # create QuadTree
    qtree = QuadTree(
        boundary=Rect(
            origin=Point(0, 0),
            width=width,
            height=height),
        capacity=5,
    )

    # fill qtree with random points
    for _ in range(args.random_points):
        qtree.insert_point(Point(
            random.randint(0, qtree.boundary.width),
            random.randint(0, qtree.boundary.height),
        ))

    # draw qtree state
    draw_qtree(surface, qtree)

    pygame.display.update()  # copy surface to display
    last_pos = pygame.mouse.get_pos()
    while True:  # loop to wait till window close
        pos = pygame.mouse.get_pos()
        if pos != last_pos:
            last_pos = pos
            clear(surface)
            query_rect_origin = (int(pos[0] - query_width / 2), int(pos[1] - query_height / 2))
            pygame.draw.rect(surface, pygame.Color('green'),
                             (query_rect_origin[0], query_rect_origin[1], query_width, query_height), 1)
            pressed = pygame.mouse.get_pressed(3)[0]

            # add new point to qtree on click
            if pressed:
                qtree.insert_point(Point(pos[0], pos[1]))
            draw_qtree(surface, qtree)

            # find points that are within that rect of the mouse
            points_in_mouse_rect = qtree.get_points_in_area(
                Rect(Point(query_rect_origin[0], query_rect_origin[1]),
                     query_width, query_height))

            for point in points_in_mouse_rect:
                pygame.draw.circle(surface, pygame.Color('green'), point.to_tuple(), 2)
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
