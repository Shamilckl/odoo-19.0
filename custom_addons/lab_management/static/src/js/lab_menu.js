/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { registry } from "@web/core/registry";

export class LabMenu extends Component {

    static template = "lab_management.LabMenu";

    static components = {
        Dropdown,
        DropdownItem,
    };

    onTestClick() {
    }

    onUsersClick() {
        this.env.services.action.doAction("base.action_res_users");
    }
}

registry.category("systray").add("lab_management.LabMenu", {
    Component: LabMenu,
});