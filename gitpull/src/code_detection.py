# apt-get install ruby ruby-dev cmake libicu-dev
# sudo gem install github-linguist

import subprocess

def determine_language(f_code):
    output = subprocess.check_output(["linguist", f_code])

    output = [x.split(':')[-1].strip().lower() 
              for x in output.split('\n')]
    
    LOC_line, type_line, mime_line, lang_line,_ = output
    sloc = LOC_line.split('(')[-1].split(' ')[0]

    stats = {
        "source_lines_of_code" : int(sloc),
        "language": lang_line,
        "mime"    : mime_line,
        "type"    : type_line
    }

    return stats


if __name__ == "__main__":
    from pprint import pprint

    print "Checking parameters for this code:"
    data = determine_language("code_detection.py")
    pprint(data)



