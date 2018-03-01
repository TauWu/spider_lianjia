#!/bin/bash

ps -ef | grep spider | grep -v git | grep -v svn | awk {'print $2, $3'}