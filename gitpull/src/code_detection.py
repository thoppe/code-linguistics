# apt-get install ruby ruby-dev cmake libicu-dev
# sudo gem install github-linguist

import subprocess

def determine_language(f_code):
    output = subprocess.check_output(["linguist", f_code])

    output = [x.split(':')[-1].strip().lower() 
              for x in output.split('\n')]
    
    sloc = output[0].split('(')[-1].split(' ')[0]

    stats = {
        "source_lines_of_code" : int(sloc),
        "type"    : output[1],
        "mime"    : output[2],
        "language": output[3],
    }

    return stats


if __name__ == "__main__":
    from pprint import pprint

    print "Checking parameters for this code:"
    data = determine_language("code_detection.py")
    pprint(data)



