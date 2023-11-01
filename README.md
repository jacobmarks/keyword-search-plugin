## Keyword Search Plugin

![keyword_search](https://github.com/jacobmarks/keyword-search-plugin/assets/12500356/08fcf04d-35c5-45e5-b950-ba732da26d14)

This plugin is a Python plugin that allows you to search through your dataset
using keywords.

## Watch On Youtube
[![Video Thumbnail](https://img.youtube.com/vi/jnNPGrM6Wr4/0.jpg)](https://www.youtube.com/watch?v=jnNPGrM6Wr4&list=PLuREAXoPgT0RZrUaT0UpX_HzwKkoB-S9j&index=6)

## Installation

```shell
fiftyone plugins download https://github.com/jacobmarks/keyword-search-plugin
```

## Operators

### `search_by_keyword`

**Description**: Search for samples by keyword

**Inputs**:

- `query`: The keyword or keyphrase to search for
- `field`: The field to search in (any `StringField`)
- `case_sensitive`: Whether to match case sensitively
