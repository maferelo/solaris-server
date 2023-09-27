# Codemaker

Create boilerplate code for a given task.

## Setup

### Copy OpenAI api key

```bash
    cp .env.template .env
```

### Install dependencies

```bash
   poetry install
```

## Usage

### Create new code

#### Create prompt

```bash
    cd projects
    mkdir <project_name>
    touch <project_name>/prompt
```

#### Run codemaker

```bash
    poetry run gpt-engineer <project_name>
```
