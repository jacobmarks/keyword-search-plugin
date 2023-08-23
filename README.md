## Keyword Search Plugin

This plugin is a Python plugin that allows you to search through your dataset using keywords.

It demonstrates how to do the following:

- Cache user choices in a Python plugin
- Use `ctx.dataset` in `resolve_input()` to access the dataset
- Set an icon for operators in the operator list
- Place operators in the action menu from Python

## Installation

```shell
fiftyone plugins download https://github.com/jacobmarks/keyword-search-plugin
```

## Operators

### `search_by_keyword`

**Description**: Search for samples by keyword

**Inputs**:

- `query`: The keyword or keyphrase to search for
- `field`: The field to search in (from top-level string fields)
- `case_sensitive`: Whether to match case sensitively
