
import sys
import os

from Foundation import NSString, NSUTF8StringEncoding
from AppKit import NSPasteboard, NSPasteboardItem
from bs4 import BeautifulSoup

import pypandoc

UTI_MARKDOWN = 'public.utf8-plain-text'

def main():
    text_original = sys.stdin.read()
    text_html = make_html(text_original)
    copy(
            ('public.html', text_html),
            (UTI_MARKDOWN, text_original),
            )

def make_html(text):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    style_file = 'styles/style.css'

    extra_args = [
            '--resource-path',
            dir_path,
            ]

    style_headers = [
            '--include-in-header',
            '--css',
            ]

    for header in style_headers:
        extra_args.append(f"{header}={style_file}")

    extensions = get_pandoc_extensions()

    output = pypandoc.convert_text(
            text,
            format = f"markdown+{extensions}",
            to = "html5",
            extra_args = extra_args,
            )

    soup = BeautifulSoup(output, 'html.parser')

    del soup['title']

    return str(soup)


def copy(*entries):
    pb = NSPasteboard.generalPasteboard()

    types = [e[0] for e in entries]
    pb.declareTypes_owner_(types, None)

    pb_item = NSPasteboardItem.alloc().init()

    for (uti, value) in entries:
        new_str = NSString.stringWithString_(value).nsstring()
        new_data = new_str.dataUsingEncoding_(NSUTF8StringEncoding)
        pb_item.setData_forType_(new_data, uti)

    pb.writeObjects_([pb_item])

def get_pandoc_extensions():
    extensions = '+'.join(
            [
                'all_symbols_escapable',
                'auto_identifiers',
                'backtick_code_blocks',
                'blank_before_blockquote',
                'blank_before_header',
                'definition_lists',
                'escaped_line_breaks',
                'example_lists',
                'fancy_lists',
                'fancy_lists',
                'fenced_code_attributes',
                'fenced_code_blocks',
                'footnotes',
                'grid_tables',
                'header_attributes',
                'implicit_figures',
                'implicit_header_references',
                'inline_code_attributes',
                'intraword_underscores',
                'line_blocks',
                'multiline_tables',
                'pandoc_title_block',
                'pipe_tables',
                'shortcut_reference_links',
                #'smallcaps',
                'space_in_atx_header',
                'strikeout',
                'subscript',
                'superscript',
                'table_captions',
                'task_lists',
                'tex_math_dollars',
                ]
            )

    return extensions

if __name__ == "__main__":
    main()

