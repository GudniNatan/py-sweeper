import pygame
from pygame import Surface, Rect
from utils.margins import Margins
import os


def blit_left(surface: Surface, source: Surface, point: tuple):
    '''
    Blit source onto surface, where the top right point of surface is the
    given point. In other words, the surface is blitted to the left of point.
    '''
    width = source.get_rect().width
    x, y = point
    x -= width
    surface.blit(source, (x, y))


def pad(source: Surface, margins: tuple, background_color=None) -> Surface:
    '''
    Pads the source Surface by margins, a quintuple on the
    form (top, right, bottom, left), or a Margins object.
    '''
    margins = Margins(*margins)
    source_rect = source.get_rect()
    padded_rect = Rect(source_rect)
    padded_rect.w += margins.left + margins.right
    padded_rect.h += margins.top + margins.bottom
    padded_surface = Surface(padded_rect.size, pygame.SRCALPHA, 32)
    padded_surface = padded_surface.convert_alpha()
    if background_color:
        padded_surface.fill(background_color)
    padded_surface.blit(source, (margins.left, margins.top))
    return padded_surface


def pad_ip(source: Surface, margins: tuple, background_color=None):
    old_size = source.get_rect().size
    old = Surface(old_size, 0, source)
    pygame.transform.scale(source, old_size, source)
    if background_color:
        source.fill(background_color)
    else:
        source.fill((0, 0, 0, 0))
    padded_surface.blit(source, (margins.left, margins.top))


def aspect_scale(image, size):
    bx, by = size
    scale_rect = pygame.Rect(0, 0, bx, by)
    image_rect = image.get_rect()
    return pygame.transform.scale(image, image_rect.fit(scale_rect).size)


def rot_center(image, angle):
    '''rotate an image while keeping its center and size'''
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def reverse_clamp(smaller_rect, larger_rect):
    if not larger_rect.contains(smaller_rect):
        new_rect = larger_rect.copy()
        if smaller_rect.left <= larger_rect.left:
            new_rect.left = smaller_rect.left
        elif smaller_rect.right >= larger_rect.right:
            new_rect.right = smaller_rect.right
        if smaller_rect.top <= larger_rect.top:
            new_rect.top = smaller_rect.top
        elif smaller_rect.bottom >= larger_rect.bottom:
            new_rect.bottom = smaller_rect.bottom
        return new_rect
    return larger_rect


# def reverse_clamp_ip(smaller_rect, larger_rect):
#     if not larger_rect.contains(smaller_rect):
#         if smaller_rect.left <= larger_rect.left:
#             larger_rect.left = smaller_rect.left
#         elif smaller_rect.right >= larger_rect.right:
#             larger_rect.right = smaller_rect.right
#         if smaller_rect.top <= larger_rect.top:
#             larger_rect.top = smaller_rect.top
#         elif smaller_rect.bottom >= larger_rect.bottom:
#             larger_rect.bottom = smaller_rect.bottom


def reverse_clamp_ip(larger_rect: Rect, smaller_rect: Rect):
    if not larger_rect.contains(smaller_rect):
        larger_rect.left = min(larger_rect.left, smaller_rect.left)
        larger_rect.right = max(larger_rect.right, smaller_rect.right)
        larger_rect.top = min(larger_rect.top, smaller_rect.top)
        larger_rect.bottom = max(larger_rect.bottom, smaller_rect.bottom)


def push_ip(larger_rect: Rect, smaller_rect: Rect):
    '''Larger rect pushes out smaller rect via the smallest possible vector.'''
    clip = larger_rect.clip(smaller_rect)
    if not clip:
        return
    if clip.height <= clip.width:
        if smaller_rect.centery <= clip.centery:
            smaller_rect.bottom = larger_rect.top
        else:
            smaller_rect.top = larger_rect.bottom
    else:
        if smaller_rect.centerx <= clip.centerx:
            smaller_rect.right = larger_rect.left
        else:
            smaller_rect.left = larger_rect.right


def fix_path():
    '''Set the path to the main folder dir. This is kinda hacky...'''
    file_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(file_path)
    os.chdir("..")
