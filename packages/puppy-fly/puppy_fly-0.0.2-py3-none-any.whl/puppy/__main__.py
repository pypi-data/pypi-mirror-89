import argparse


def fun_gpus(args):
    print("call fun gpus")
    return args


def fun_batch_size(args):
    print("call fun batch size")
    return args


if  __name__=="__main__":
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--gpus', type=str, default=None)
    parser.add_argument('--batch-size', type=int, default=32)
    args = parser.parse_args()
    print(args.gpus, type(args.gpus))
    print(args.batch_size, type(args.batch_size))
    if args.gpus == '1':
        fun_gpus(args.gpus)
    if args.batch_size == 1:
        fun_batch_size(args.batch_size)
