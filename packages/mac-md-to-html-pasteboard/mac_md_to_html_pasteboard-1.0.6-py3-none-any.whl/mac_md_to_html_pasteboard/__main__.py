
import sys
import os

from Foundation import NSString, NSUTF8StringEncoding
from AppKit import NSPasteboard

import pypandoc

def make_html():
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

    output = pypandoc.convert_text(
            sys.stdin.read(),
            format = "md",
            to = "html5",
            extra_args = extra_args,
            )

    return output

def copy(text):
    pb = NSPasteboard.generalPasteboard()
    pb.clearContents()
    pb.declareTypes_owner_(['public.html'], None)

    new_str = NSString.stringWithString_(text).nsstring()
    new_data = new_str.dataUsingEncoding_(NSUTF8StringEncoding)
    pb.setData_forType_(new_data, 'public.html')

def main():
    text = make_html()
    copy(text)

if __name__ == "__main__":
    main()
