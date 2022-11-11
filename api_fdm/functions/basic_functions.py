import json
from datetime import datetime
from typing import Union

from jinja2 import Environment, FileSystemLoader


def debugger(api_url: str, request_text: Union[dict, str], tmp_dir: str) -> None:
    if type(request_text) is dict:
        request_text = json.dumps(request_text, indent=2)
    debug_file = f"{tmp_dir}/debug.log"
    timestamp = str(datetime.now()).split('.')[0]
    fh = open(debug_file, "a+")
    fh.write(f"\n#------------{  timestamp  }-----------#\n\n")
    fh.write(api_url)
    fh.write("\n")
    fh.write(request_text)
    fh.write("\n")
    fh.close()


def get_items_from_group(all_int_info: dict, interface_name: str) -> dict:
    if all_int_info.get("items"):
        for item in all_int_info["items"]:
            if item["name"] == interface_name:
                result = item
    return result


def check_for_errors(results_list: list) -> bool:
    result = True
    for i in results_list:
        if i in [401, 422]:
            result = False
    return result


def jijna2_to_json(template_file: str, values: dict) -> dict:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_file)
    result_from_template = template.render(values).replace("\n", "")
    data_json = json.loads(result_from_template)
    return data_json
