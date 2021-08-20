#!/bin/bash

set -xe

if [ -d quote_fetcher ]
then
  cd quote_fetcher
fi

functions-framework --target fetch_quote --debug --port 8899
