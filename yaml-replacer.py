#  Get all .yaml files in /src for replacement
#  Replace between Table{ } if match found from pattern.yaml
#  Write the new files to /dest

#  Example of pattern.yaml:
# match: '[au].[level_2]'
# from-to-list-to-replace:
#   - from: '[au].[level_2]'
#   to: '[au].[level_3]'
#   - from: 'au_prefix_2'
#   to: 'au_prefix_3'
#   - from: 'fkey201'
#   to: 'fkey202'
#   - from: 'POST'
#   to: 'GET'

# Example of a to replace table:
# Table({
#     ID202: GUID(),
#     au_prefix_2:
#     Concatenate(varSelectedCore.au_prefix_1,".",Text(CountRows(Filter('au.level_2',fkey201 = varSelectedCore.ID201)) + 1)),
#     au_level_2: Trim('2011_TextL2-18_1'.Text),
#     fkey201: varSelectedCore.ID201,
#     auth: "*",
#     tableName: "[au].[level_2]",
#     type: "POST",
#     UPN: User().Email
# })

# Example of a replaced table:
# Table({
#     ID202: GUID(),
#     au_prefix_3:
#     Concatenate(varSelectedCore.au_prefix_1,".",Text(CountRows(Filter('au.level_2',fkey201 = varSelectedCore.ID201)) + 1)),
#     au_level_2: Trim('2011_TextL2-18_1'.Text),
#     fkey202: varSelectedCore.ID201,
#     auth: "*",
#     tableName: "[au].[level_3]",
#     type: "GET",
#     UPN: User().Email
# })


import os
import sys
import yaml
import re
import glob

def main():
    # parser = argparse.ArgumentParser(description='Replace from to in yaml files')
    # parser.add_argument('-s', '--src', help='Source path', required=True)
    # parser.add_argument('-d', '--dest', help='Destination path', required=True)
    # parser.add_argument('-p', '--pattern', help='Pattern file', required=True)
    # args = parser.parse_args()

    src = 'src'
    dest = 'dest'
    pattern = 'pattern.yaml'

    if not os.path.exists(src):
        print("Source path does not exist")
        sys.exit(1)

    if not os.path.exists(pattern):
        print("Pattern file does not exist")
        sys.exit(1)

    if not os.path.exists(dest):
        print("Destination path does not exist, creating it")
        os.makedirs(dest)

    if os.listdir(dest):
        print("Destination path is not empty, do you want to continue? (y/n)")
        answer = input()
        if answer != "y":
            sys.exit(1)

    for filename in glob.glob(os.path.join(src, '*.yaml')):
        print("Processing file: " + filename)
        with open(filename, 'r') as file:
            filedata = file.read()
            with open(pattern, 'r') as pattern_file:
                pattern_data = yaml.load(pattern_file, Loader=yaml.FullLoader)
                match = pattern_data['match']
                from_to_list = pattern_data['from-to-list-to-replace']
                for from_to in from_to_list:
                    from_str = from_to['from']
                    to_str = from_to['to']
                    # replace between Table{ } only if match found between Table{ }
                    filedata = re.sub(r'Table\({(.*?)}\)', lambda x: replace_between(x, match, from_str, to_str), filedata, flags=re.DOTALL)
        with open(os.path.join(dest, os.path.basename(filename)), 'w') as file:
            file.write(filedata)

def replace_between(match, match_str, from_str, to_str):
    if match_str in match.group(1):
        return match.group(0).replace(from_str, to_str)
    else:
        return match.group(0)

if __name__ == "__main__":
    main()





