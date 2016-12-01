#!/bin/bash

set -e

cd $(dirname $0)/..

wget -c -P src/lib/ http://www.unicode.org/Public/UNIDATA/UnicodeData.txt
wget -c -P src/lib-fts/ http://www.unicode.org/Public/UNIDATA/auxiliary/WordBreakProperty.txt
wget -c -P src/lib-fts/ http://www.unicode.org/Public/UNIDATA/PropList.txt

#eof
