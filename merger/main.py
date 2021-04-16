import os
import shutil
from pathlib import Path


def get_main_latex(arr):
    flag = False
    arr_out = []
    for i in range(len(arr)):
        if '\\begin{document}' in arr[i]:
            flag = True
        if '\\end{document}' in arr[i]:
            flag = False
        if flag and '\\begin{document}' not in arr[i]:
            arr_out.append(arr[i])
    return arr_out


Path("images/").mkdir(parents=True, exist_ok=True)

home_path = str(Path(__file__).resolve().parent).replace('\\', '/').split('/')

semesters = list(filter(lambda x: os.path.exists(os.path.join(
    '/'.join(home_path[:-1]), x)), ['first_semester', 'second_semester']))

assert len(
    semesters) > 0, "[ERROR] You have no 'first_semester' or 'second_semester' folders!"

for sem in semesters:
    lections = os.listdir(os.path.join('/'.join(home_path[:-1]), sem))

    assert "title" in lections, f"[ERROR] You have no 'title' folder in '{sem}'"

    del lections[lections.index('title')]
    if 'appendix' in lections:
        del lections[lections.index('appendix')]
        lections.sort(key=int)
        lections = ['title'] + lections + ['appendix']
    else:
        lections.sort(key=int)
        lections = ['title'] + lections

    lections_inside = {}

    for l in lections:
        assert 'main.tex' in os.listdir(os.path.join(
            '/'.join(home_path[:-1]), sem, l)), f"[ERROR] No 'main.tex' found in {sem}/{l}"
        with open(os.path.join('/'.join(home_path[:-1]), sem, l, 'main.tex'), 'r', encoding='utf-8') as f:
            lections_inside[l] = f.readlines()

    f = open(os.path.join('/'.join(home_path),
             sem + '.tex'), 'w', encoding='utf-8')

    # getting packages names'
    packages = set()

    for key in lections_inside:
        for i in range(len(lections_inside[key])):
            if '\\usepackage' in lections_inside[key][i]:
                packages.add(lections_inside[key][i].replace(
                    '} \n', '}\n').replace('] \n', ']\n'))

    packages = sorted(list(packages))

    # pre
    f.write('\\documentclass{article}\n')
    f.write('\n')
    f.writelines(packages)
    f.write('\n')
    f.write('\\hypersetup{ colorlinks=true, linktoc=all, linkcolor=blue, }\n')
    f.write('\n')
    f.write('\\pagenumbering{arabic}\n')
    f.write('\n')
    f.write('\\begin{document}\n')

    # title page
    f.writelines(get_main_latex(lections_inside['title']))
    f.write('\t\\newpage\n')
    del lections_inside['title']

    # toc page
    f.write('\t\\tableofcontents\n')
    f.write('\t\\thispagestyle{empty}\n')
    f.write('\t\\setcounter{tocdepth}{5}\n')
    f.write('\t\\newpage\n')

    # pages
    for key in lections_inside:
        # copying images
        if 'images' in os.listdir(os.path.join('/'.join(home_path[:-1]), sem, l)):
            for fs in os.listdir(os.path.join('/'.join(home_path[:-1]), sem, l, 'images')):
                shutil.copy(os.path.join('/'.join(home_path[:-1]), sem, l, 'images', fs), os.path.join('/'.join(home_path), 'images/', fs))
        # writing pages
        f.writelines(get_main_latex(lections_inside[key]))
        # f.write('\t\\newpage\n')

    # post
    f.write('\\end{document}\n')
    f.close()
