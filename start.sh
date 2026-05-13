#!/bin/bash
echo "Запуск микросервисов"
python currency_manager.py &
python data_manager.py &
python gateway.py &

wait
