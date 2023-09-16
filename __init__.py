"""Keyword Search plugin.

| Copyright 2017-2023, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""

import json
import os

from bson import json_util

import fiftyone as fo
from fiftyone.core.utils import add_sys_path
import fiftyone.operators as foo
from fiftyone.operators import types
from fiftyone import ViewField as F


def _is_teams_deployment():
    val = os.environ.get("FIFTYONE_INTERNAL_SERVICE", "")
    return val.lower() in ("true", "1")


TEAMS_DEPLOYMENT = _is_teams_deployment()

if not TEAMS_DEPLOYMENT:
    with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
        # pylint: disable=no-name-in-module,import-error
        from cache_manager import get_cache


def serialize_view(view):
    return json.loads(json_util.dumps(view._serialize()))


def get_string_fields(dataset):
    """Get all string fields in a dataset."""
    string_fields = []
    fields = dataset.get_field_schema(flat=True)
    for field, ftype in fields.items():
        full_type = str(ftype)
        if "StringField" in full_type:
            string_fields.append(field)
    return string_fields


def _is_label_field(dataset, field):
    if "." not in field:
        return False
    else:
        sample = dataset.first()
        outer_field = field.split(".")[0]
        return "label" in str(type(sample[outer_field]))


def _is_list_field(dataset, field):
    return "ListField" in str(type(dataset.get_field_schema(flat=True)[field]))


def generate_query(dataset, field, keyword, case_sensitive):
    """Generate a query for a sample."""

    label_flag = _is_label_field(dataset, field)
    list_flag = _is_list_field(dataset, field)

    if not label_flag and not list_flag:
        return dataset.match(
            F(field).contains_str(keyword, case_sensitive=case_sensitive)
        )
    elif list_flag and not label_flag:
        return dataset.match(
            F(field)
            .join("")
            .contains_str(keyword, case_sensitive=case_sensitive)
        )
    elif label_flag:
        outer_field = field.split(".")[0]
        inner_field = ".".join(field.split(".")[2:]).strip()
        return dataset.match_labels(
            filter=F(inner_field).contains_str(
                keyword, case_sensitive=case_sensitive
            ),
            fields=outer_field,
        )
    else:
        outer_field = field.split(".")[0]
        inner_field = ".".join(field.split(".")[2:]).strip()
        return dataset.match_labels(
            filter=F(inner_field)
            .join("")
            .contains_str(keyword, case_sensitive=case_sensitive),
            fields=outer_field,
        )


class KeywordSearch(foo.Operator):
    @property
    def config(self):
        _config = foo.OperatorConfig(
            name="search_by_keyword",
            label="Keyword Search: Find samples with keyword",
            dynamic=True,
        )
        _config.icon = "/assets/icon_white.svg"
        return _config

    def resolve_placement(self, ctx):
        return types.Placement(
            types.Places.SAMPLES_GRID_ACTIONS,
            types.Button(
                label="Search by keyword",
                icon="/assets/icon_white.svg",
                dark_icon="/assets/icon.svg",
                light_icon="/assets/icon_white.svg",
                prompt=True,
            ),
        )

    def resolve_input(self, ctx):
        inputs = types.Object()
        form_view = types.View(
            label="Keyword Search", description="Return samples with keyword"
        )

        string_fields = get_string_fields(ctx.dataset)

        if not TEAMS_DEPLOYMENT:
            cache = get_cache()
            if "field" in cache:
                default_field = cache["field"]
            else:
                default_field = string_fields[0]
        else:
            default_field = string_fields[0]

        field_dropdown = types.Dropdown(label="Field to search within")
        for sf in string_fields:
            field_dropdown.add_choice(sf, label=sf)

        inputs.enum(
            "search_field",
            field_dropdown.values(),
            default=default_field,
            view=field_dropdown,
        )

        inputs.bool(
            "case_sensitive",
            label="Case sensitive",
            default=False,
        )

        new_default_field = ctx.params.get("search_field", "none")
        get_cache()["field"] = new_default_field

        inputs.str("keyword", label="Query", required=True)
        return types.Property(inputs, view=form_view)

    def execute(self, ctx):
        keyword = ctx.params["keyword"]
        field = ctx.params["search_field"]
        case_sensitive = ctx.params["case_sensitive"]
        view = generate_query(ctx.dataset, field, keyword, case_sensitive)
        ctx.trigger(
            "set_view",
            params=dict(view=serialize_view(view)),
        )
        ctx.trigger("reload_dataset")
        return


def register(plugin):
    plugin.register(KeywordSearch)
