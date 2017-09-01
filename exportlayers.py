#!/usr/bin/env python

"""
Export selected layers from Inkscape SVG.
"""

from xml.dom import minidom
import codecs


def export_layers(src, dest, hide, show, hide_all, print_layers, leave):
    """
    Export selected layers of SVG in the file `src` to the file `dest`.

    :arg  str    src:  path of the source SVG file.
    :arg  str   dest:  path to export SVG file.
    :arg  list  hide:  layers to hide. each element is a string.
    :arg  list  show:  layers to show. each element is a string.

    """
    svg = minidom.parse(open(src))
    g_hide = []
    g_show = []
    for g in svg.getElementsByTagName("g"):
        if g.attributes.has_key("inkscape:label"):
            label = g.attributes["inkscape:label"].value
            if print_layers:
                print(label)
            if label in hide or hide_all:
                g.attributes['style'] = 'display:none'
                g_hide.append(g)
            elif label in show:
                g.attributes['style'] = 'display:inline'
                g_show.append(g)
            elif label not in leave and leave:
                parent = g.parentNode
                parent.removeChild(g)
    export = svg.toxml()
    if dest:
        codecs.open(dest, "w", encoding="utf8").write(export)
        print("Hide {0} node(s);  Show {1} node(s).".format(
            len(g_hide), len(g_show)))


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        '--hide', action='append', default=[],
        help='layer to hide. this option can be specified multiple times.')
    parser.add_argument(
        '--hide_all', action='store_true',
        help='hide all layers.')
    parser.add_argument(
        '--print_layers', action='store_true',
        help='print a list of layers in a file.')
    parser.add_argument(
        '--show', action='append', default=[],
        help='layer to show. this option can be specified multiple times.')
    parser.add_argument(
        '--leave', action='append', default=[],
        help='layer to not delete. this option can be specified multiple times.')
    parser.add_argument('src', help='source SVG file.')
    parser.add_argument('dest', nargs='?', default=None,
        help='path to export SVG file.')
    args = parser.parse_args()
    export_layers(**vars(args))


if __name__ == '__main__':
    main()
