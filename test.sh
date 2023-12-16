#!/bin/bash

echo "Stopping ruokalista service and starting testing..."
sudo systemctl stop ruokalista-aanestyspaate.service
python3 test.py
echo "test exited. Starting ruokalista service back up"
sudo systemctl start ruokalista-aanestyspaate.service
sleep 1
sudo systemctl status ruokalista-aanestyspaate.service
