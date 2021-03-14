import getopt
import sys

from gpu import GPU, Status


def startup():
    print("Auto select GPU")
    e_gpu = GPU.e_gpu()
    i_gpu = GPU.i_gpu()
    if e_gpu.status == Status.Missing:
        i_gpu.enable()
    else:
        e_gpu.enable()
        i_gpu.disable()


def select_card(card):
    print(f"Select card: {card}")
    e_gpu = GPU.e_gpu()
    i_gpu = GPU.i_gpu()
    if card == "eGPU":
        e_gpu.enable()
        i_gpu.disable()
    elif card == "iGPU":
        i_gpu.enable()
        e_gpu.disable()
    else:
        raise Exception(f"Unknown card: {card}")


def get_gpu(card) -> GPU:
    if card == "eGPU":
        return GPU.e_gpu()
    elif card == "iGPU":
        return GPU.i_gpu()
    else:
        raise Exception(f"Unknown card: {card}")


def main(argv):
    opts, args = getopt.getopt(argv, "sc:e:d:", ["startup", "card=", "enable=", "disable="])
    if len(opts) == 1:
        opt, arg = opts[0]
        if opt in ("-s", "--startup"):
            startup()
        elif opt in ("-c", "--card"):
            select_card(arg)
        elif opt in ("-e", "--enable"):
            get_gpu(arg).enable()
        elif opt in ("-d", "--disable"):
            get_gpu(arg).disable()
        else:
            raise Exception(f"Unknown argument: {opt}")
    else:
        raise Exception(f"Unexpected argument length: {len(opts)}")


if __name__ == '__main__':
    main(sys.argv[1:])

