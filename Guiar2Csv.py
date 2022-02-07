import logging
import os

from util.guiar import export_from_guiar

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
uid = input("UID: ")
uid = uid.strip()
input_dir = "gar/record"
output_dir = "gar/record/csv"
input_path = os.path.join(input_dir, f"{uid}.guiar")
output_path = os.path.join(output_dir, f"{uid}.csv")
try:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    export_from_guiar(input_path, output_path)
except Exception as e:
    import traceback

    logging.error(traceback.format_exc())
else:
    logging.info(f"文件已生成于{os.path.abspath(output_path)}")
os.system('pause')
