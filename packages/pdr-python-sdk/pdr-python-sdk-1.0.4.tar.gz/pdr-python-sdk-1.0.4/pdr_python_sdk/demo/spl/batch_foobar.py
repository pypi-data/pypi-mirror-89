#!/usr/bin/env python

import sys

from ...spl import SplStreamingBatchCommand
from ...on_demand_action import run

class Foobar(SplStreamingBatchCommand):
    def streaming_handle(self, lines):
        for line in lines:
            line['foo'] = 'bar'
        return lines


if __name__ == '__main__':
    run(Foobar, sys.argv, sys.stdin.buffer, sys.stdout.buffer)