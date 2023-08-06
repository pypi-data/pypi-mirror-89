import click
import requests
import json
import os


@click.group()
def cli():
    pass


@click.command()
@click.option('--config', help="nni config")
@click.option('--port', default=1234, help="nni port")
def run(port,config):
    try:
        path = os.path.exists(config)
        if path is False:
            print("path check!!!")
            return
        file_path = config
        with open(file_path, "r") as yaml:
            load_data = yaml.read()
        json_data = json.dumps(load_data)
        url_items = "http://211.180.114.176:31778/nni/run/{}".format(port)
        response = requests.post(url_items,json=json_data)

        if "app.nni.ApiError" in response.text:
            print("config parsing error")
        else:
            print(response.text)
    except Exception as error:
        print(error)


@click.command()
def experiment():
    url_items = "http://211.180.114.176:31778/nni/experiment/list"
    response = requests.get(url_items)
    print(response.text)


@click.command()
@click.argument('id')
def trial(id):
    url_items = "http://211.180.114.176:31778/nni/trial/ls/{}".format(id)
    response = requests.get(url_items)
    print(response.text)


@click.command()
@click.option('--eid', help="nni experimentid")
@click.option('--tid', help="nni trialid")
def trial_kill(eid, tid):
    url_items = "http://211.180.114.176:31778/nni/trial/kill/{}/{}".format(eid,tid)
    response = requests.get(url_items)
    if "app.nni.ApiError" in response.text:
        print("experiment id or trial id check")
    else:
        print(response.text)


@click.command()
@click.argument('id')
def stop(id):
    url_items = "http://211.180.114.176:31778/nni/stop/{}".format(id)
    response = requests.get(url_items)
    print(response.text)


@click.command()
def stop_all():
    url_items = "http://211.180.114.176:31778/nni/stop/all"
    response = requests.get(url_items)
    print(response.text)


@click.command()
@click.argument('id')
def log_stdout(id):
    url_items = "http://211.180.114.176:31778/nni/log/stdout/{}".format(id)
    response = requests.get(url_items)
    print(response.text)


@click.command()
@click.argument('id')
def log_stderr(id):
    url_items = "http://211.180.114.176:31778/nni/log/stderr/{}".format(id)
    response = requests.get(url_items)
    print(response.text)


def main():
    #sodaflow run --port 1231
    cli.add_command(run)
    #sodaflow experiment
    cli.add_command(experiment)
    #sodaflow trial id
    cli.add_command(trial)
    #sodaflow trial kill id
    cli.add_command(trial_kill)
    #sodaflow stop id
    cli.add_command(stop)
    #sodaflow stop-all
    cli.add_command(stop_all)
    # sodaflow log-stdout id
    cli.add_command(log_stdout)
    # sodaflow log-stderr id
    cli.add_command(log_stderr)
    cli()


if __name__ == '__main__':
    main()
