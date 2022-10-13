# Get all .yaml files in /src for replacement
# Replace between Table{ } if match found from pattern.yaml
# Write the new files to /dest

# Read the pattern file Replacements Extract.xlsx
# Example of Replacements Extract.xlsx:

# matcher,replace,
# matcher,from,to
# [au].[level_2],ID201,Id

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
#     ID: GUID(),
#     au_prefix_2:
#     Concatenate(varSelectedCore.au_prefix_1,".",Text(CountRows(Filter('au.level_2',fkey201 = varSelectedCore.ID201)) + 1)),
#     au_level_2: Trim('2011_TextL2-18_1'.Text),
#     fkey202: varSelectedCore.ID201,
#     auth: "*",
#     tableName: "[au].[level_2]",
#     type: "POST",
#     UPN: User().Email
# })

import os
import re
import glob
import pandas as pd

def main():
    # parser = argparse.ArgumentParser(description='Replace from to in yaml files')
    # parser.add_argument('-s', '--src', help='Source path', required=True)
    # parser.add_argument('-d', '--dest', help='Destination path', required=True)
    # parser.add_argument('-p', '--pattern', help='Pattern file', required=True)
    # args = parser.parse_args()

    src = 'src'
    dest = 'dest'
    pattern = 'Replacements Extract.xlsx'

    # Read the pattern file from the first tab from the row witch hs matcher,from,to
    df = pd.read_excel(pattern, sheet_name=0, skiprows=1)

    # Get all .yaml files in /src for replacement
    files = glob.glob(src + '/*.yaml')

    # Replace between Table{ } if match found from pattern.yaml
    for file in files:
        with open(file, 'r') as f:
            filedata = f.read()

            # Replace the table
            for index, row in df.iterrows():
                match = row['matcher']
                from_str = row['from']
                to_str = row['to']

                filedata = re.sub(r'Table\({(.*?)}\)', lambda x: replace_between(x, match, from_str, to_str), filedata, flags=re.DOTALL)

            # Write the new files to /dest
            with open(dest + '/' + os.path.basename(file), 'w') as f:
                f.write(filedata)  


def replace_between(match, match_str, from_str, to_str):
    if match_str in match.group(1):
        print("Replacing " + from_str + " with " + to_str + " in " + match.group(1))
        return match.group(0).replace(from_str, to_str)
    else:
        return match.group(0)

if __name__ == '__main__':
    main()
    




