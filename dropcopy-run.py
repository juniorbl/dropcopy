#!/usr/bin/env python

import gobject

from dropcopy.dropcopy import Dropcopy

if __name__ == "__main__":
	gobject.threads_init()
	Dropcopy()
