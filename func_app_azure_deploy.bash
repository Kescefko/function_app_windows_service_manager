#!/bin/bash

az functionapp create \
  --resource-group rg-gyorgy-shared-dev \
  --consumption-plan-location germanywestcentral \
  --runtime python \
  --runtime-version 3.10 \
  --name func-gyorgy-shared-dev \
  --storage-account stgyorgyfuncdev \
  --os-type Linux
