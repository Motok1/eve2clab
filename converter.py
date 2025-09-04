import unl2clab
import argparse
from enum import Enum

class ConvertMode(Enum):
     MODE_UNL2CLAB = "unl2clab"
     MODE_CLAB2UNL = "clab2unl"

if __name__ == '__main__':

    choices = [mode.value for mode in ConvertMode]

    # argparseの設定
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",
                        choices=choices,
                        default=ConvertMode.MODE_UNL2CLAB.value)
    parser.add_argument("-f", "--file",
                        type=str, default="sample.unl")
    args = parser.parse_args()

    file_path = args.file

    if args.mode == ConvertMode.MODE_UNL2CLAB.value:
        unl2clab.convert_unl_to_clab(file_path)
    elif args.mode == ConvertMode.MODE_CLAB2UNL.value:
        raise NotImplementedError("clab2unl is not implemented yet.")
