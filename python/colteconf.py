#!/usr/bin/env python3

import ruamel.yaml
import os

import colteconf_cn_4g as colte_cn
import colteconf_prepaid as colte_prepaid

# This version saves comments/edits in YAML files
yaml = ruamel.yaml.YAML()
yaml.indent(sequence=4, mapping=2, offset=2)

# Input
colte_vars = "/etc/colte/config.yml"

if __name__ == "__main__":
    RED = "\033[0;31m"
    NC = "\033[0m"

    if os.geteuid() != 0:
        print("colteconf: ${RED}error:${NC} Must run as root! \n")
        exit(1)

    # Read old vars and update yaml
    with open(colte_vars, "r") as file:
        colte_data = yaml.load(file.read())

        colte_cn.update_all_components(colte_data)
        colte_prepaid.update_all_components(colte_data)

    # Restart everything to pick up new configurations, and don't restart
    # networkd while the EPC or metering are running.
    colte_cn.stop_all_services()
    colte_prepaid.stop_all_services()
    os.system("systemctl restart systemd-networkd")

    colte_cn.sync_service_state(colte_data)
    colte_prepaid.sync_service_state(colte_data)
