import os


# def create_dirs(parent_dir, companies_names, stage_names):
#     for comp_name in companies_names:
#         for stage_name in stage_names:
#             Path(os.path.join(parent_dir, comp_name, stage_name)) \
#                 .mkdir(parents=True, exist_ok=True)

def write_response_content(dir_path, company, stage, content, page=1):
    fname = os.path.join(dir_path, f'{company}__{stage}__{page}.html')
    with open(fname, 'wb') as out_html:
        out_html.write(content)

