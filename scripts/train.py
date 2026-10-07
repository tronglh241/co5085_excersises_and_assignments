import argparse

from common.config.config import CfgNode

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    args = parser.parse_args()

    cfg = CfgNode.load(args.config)
    cfg.trainer.run()
