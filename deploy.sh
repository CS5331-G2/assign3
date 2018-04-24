#!/bin/bash

ansible-playbook -i inventory/production.hosts production.yml --ask-become-pass