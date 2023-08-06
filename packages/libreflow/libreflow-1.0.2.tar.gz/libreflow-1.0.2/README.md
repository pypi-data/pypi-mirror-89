# libreflow

LibreFlow is a project flow made for [https://gitlab.com/kabaretstudio/kabaret](Kabaret studio)


## Install

>  pipenv install -e "git+https://gitlab.com/lfs.coop/libreflow.git@pippackage#egg=libreflow" --pre

Currently we need the --pre to allow pre releases, which is requiered to get the last version of Kabaret.

## Run

>  pipenv run python -m libreflow.gui --host yourRedisHost --port 6379 --db 0 --cluster xxx --session xx


