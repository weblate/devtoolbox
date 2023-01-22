# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio, GObject
from .widgets.sidebar_item import SidebarItem
from .views.tab_content import TabContent
from .views.json_yaml import JsonYamlView
from .views.timestamp import TimestampView


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/window.ui')
class DevtoolboxWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DevtoolboxWindow'

    # Template elements
    _flap_btn   = Gtk.Template.Child()
    _tabs_stack = Gtk.Template.Child()

    # GSettings
    _settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self, debug, **kwargs):
        super().__init__(**kwargs)

        # Theme headerbar
        if debug == "False":
            self.remove_css_class("devel")

        tools = {
            "json-yaml": {
                "title": _("JSON - YAML"),
                "category": "converter",
                "icon-name": "horizontal-arrows-symbolic",
                "child": JsonYamlView()
            },
            "timestamp": {
                "title": _("Timestamp"),
                "category": "converter",
                "icon-name": "hourglass-symbolic",
                "child": TimestampView()
            },
            "encoder": {
                "title": _("Encoder"),
                "category": "encoder",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="Encoder")
            },
            "formatter": {
                "title": _("formatter"),
                "category": "formatter",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="formatter")
            },
            "generator": {
                "title": _("generator"),
                "category": "generator",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="generator")
            },
            "text": {
                "title": _("text"),
                "category": "text",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="text")
            },
            "graphic": {
                "title": _("graphic"),
                "category": "graphic",
                "icon-name": "clock-rotate-symbolic",
                "child": Gtk.Label(label="graphic")
            }
        }

        categories = {
            "converter": {
                "title": _("Converters"),
                "icon-name": "horizontal-arrows-symbolic",
                "child": TabContent(self._get_tools(tools, "converter"))
            },
            "encoder": {
                "title": _("Encoders"),
                "icon-name": "folder-templates-symbolic",
                "child": TabContent(self._get_tools(tools, "encoder"))
            },
            "formatter": {
                "title": _("Formatters"),
                "icon-name": "text-indent-symbolic",
                "child": TabContent(self._get_tools(tools, "formatter"))
            },
            "generator": {
                "title": _("Generators"),
                "icon-name": "plus-symbolic",
                "child": TabContent(self._get_tools(tools, "generator"))
            },
            "text": {
                "title": _("Text"),
                "icon-name": "text-ab-symbolic",
                "child": TabContent(self._get_tools(tools, "text"))
            },
            "graphic": {
                "title": _("Graphics"),
                "icon-name": "brush-symbolic",
                "child": TabContent(self._get_tools(tools, "graphic"))
            }
        }

        # Setup tabs
        for c in categories:
            self._tabs_stack.add_named(categories[c]["child"], c)
            page = self._tabs_stack.get_page(categories[c]["child"])
            page.set_title(categories[c]["title"])
            page.set_icon_name(categories[c]["icon-name"])
            if c != "favorite":
                self._flap_btn.bind_property("active", page.get_child().get_flap(), "reveal-flap", GObject.BindingFlags.SYNC_CREATE)
                page.get_child().get_flap().bind_property("reveal-flap", self._flap_btn, "active", GObject.BindingFlags.SYNC_CREATE)

        # Restore last state
        self._settings.bind("window-width",     self,           "default-width",  Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("window-height",    self,           "default-height", Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("window-maximized", self,           "maximized",      Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("sidebar-open",     self._flap_btn, "active",         Gio.SettingsBindFlags.DEFAULT)
        self._settings.bind("last-tab",         self._tabs_stack, "visible-child-name", Gio.SettingsBindFlags.DEFAULT)

        content_stack = self._tabs_stack.get_visible_child().get_content_stack()
        self._settings.bind("last-tool", content_stack, "visible-child-name", Gio.SettingsBindFlags.DEFAULT)


    def _on_flap_btn_clicked(self, data):
        self._flap.set_reveal_flap(self._flap_btn.get_active())

    def _get_tools(self, tools: dict, category: str):
        tools_in_category = {}
        for t in tools:
            if tools[t]["category"] == category:
                tools_in_category[t] = tools[t]
        return tools_in_category

    
