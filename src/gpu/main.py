import getopt
import sys
import subprocess

from elevate import elevate

from gpu import GPU, Status


def startup() -> bool:
    print("Auto select GPU")
    e_gpu = GPU.e_gpu()
    i_gpu = GPU.i_gpu()
    return_value = False
    if e_gpu.status == Status.Missing:
        return_value = return_value or i_gpu.enable()
    else:
        return_value = return_value or e_gpu.enable()
        return_value = return_value or i_gpu.disable()
    return return_value


def select_card(card) -> bool:
    print(f"Select card: {card}")
    e_gpu = GPU.e_gpu()
    i_gpu = GPU.i_gpu()
    return_value = False
    if card == "eGPU":
        return_value = return_value or e_gpu.enable()
        return_value = return_value or i_gpu.disable()
    elif card == "iGPU":
        return_value = return_value or i_gpu.enable()
        return_value = return_value or e_gpu.disable()
    else:
        raise Exception(f"Unknown card: {card}")
    return return_value


def get_gpu(card) -> GPU:
    if card == "eGPU":
        return GPU.e_gpu()
    elif card == "iGPU":
        return GPU.i_gpu()
    else:
        raise Exception(f"Unknown card: {card}")


def main(argv) -> bool:
    opts, args = getopt.getopt(argv, "sc:e:d:", ["startup", "card=", "enable=", "disable="])
    if len(opts) == 1:
        opt, arg = opts[0]
        if opt in ("-s", "--startup"):
            return startup()
        elif opt in ("-c", "--card"):
            return select_card(arg)
        elif opt in ("-e", "--enable"):
            return get_gpu(arg).enable()
        elif opt in ("-d", "--disable"):
            return get_gpu(arg).disable()
        else:
            raise Exception(f"Unknown argument: {opt}")
    else:
        raise Exception(f"Unexpected argument length: {len(opts)}")


if __name__ == '__main__':
    elevate()
    timeout = 60
    try:
        log_interesting = main(sys.argv[1:])
        if not log_interesting:
            timeout = 10
    except Exception as e:
        print(e)
    finally:
        subprocess.run(f"timeout {timeout}")
