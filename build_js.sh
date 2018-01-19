#!/bin/sh
cd js
yarn build-prod
mv dist/* ../report_builder/static/report_builder/
