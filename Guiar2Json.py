import logging
import os

from util.guiar import export_from_guiar

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
uid = input("UID: ")
uid = uid.strip()
input_dir = "gar/record"
input_path = os.path.join(input_dir, f"{uid}.guiar")
try:
    output_path, output_path_incomplete = export_from_guiar(input_path, output_format="json")
except Exception as e:
    import traceback

    logging.error(traceback.format_exc())
else:
    logging.info(f"文件已生成于{output_path,output_path_incomplete}")
os.system('pause')
