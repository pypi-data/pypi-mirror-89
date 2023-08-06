# [WIP] Clickhouse Migration 

Currently, in active development

A Clickhouse migration tools written in Python.

A tool to manage migrations on Clickhouse using clickhouse-driver

## Inspirations
golang-migrate

## Features
- Support data replication

## TODO
- Tests
- Support prefetching migrations for heavy sources
- Add S3 Source
- Add doc
- Complete exceptions
- Replace cerberus by pydantic
- Implement the graceful stop (finish operations if cancel is requested)