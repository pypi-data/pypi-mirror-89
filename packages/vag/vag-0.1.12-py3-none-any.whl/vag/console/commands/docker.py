import os
import click
import sys
from jinja2 import Template
from vag.utils import config
from vag.utils import exec

@click.group()
def docker():
    """ Docker automation """
    pass


@docker.command()
@click.argument('name', default='', metavar='<service>')
@click.option('--debug', is_flag=True, default=False, help='debug this command')
def deploy(name, debug):
    """builds running vagrant instances"""

    # password-dev:0.8.4
    service = name[:name.rfind('-')]
    group = name[name.rfind('-')+1:name.rfind(':')]
    version = name[name.rfind(':')+1:]

    image = f'docker-registry.7onetella.net:5000/7onetella/{service}:{version}'

    template = Template("""
    job "{{ service }}" {
      datacenters = ["dc1"]

      type = "service"

      update {
        stagger      = "30s"
        max_parallel = 1
      }

      group "{{ group }}" {
        count = 1
        network {
            port "http" { to = {{ port }} }
        }            
            
        task "service" {
            driver = "docker"
            config {
                image = "{{ image }}"
                ports = [ "http" ]
            }
    
            resources {
                cpu = 20
                memory = {{ memory }}
            }
    
            service {
                tags = ["urlprefix-{{ service }}-{{ group }}.7onetella.net/"]
                port = "http"
                check {
                    type     = "http"
                    path     = "{{ health_check }}"
                    interval = "10s"
                    timeout  = "2s"
                }
            }
    
            env {  {% for key, value in envs.items() %}
                {{ key }} = "{{ value }}"{% endfor %}                
            }
        }
      }
    }""")

    current_dir = os.getcwd()
    app_file = f'{current_dir}/{service}-{group}.app'
    data = config.read(app_file)
    if debug:
        print(f'data is \n {data}')

    try:
        os.makedirs(f'/tmp/nomad')
    except OSError:
        # do nothing
        pass

    output = template.render(
        service=service,
        group=group,
        image=image,
        memory=get(data, 'memory', 128),
        port=get(data, 'port', 4242),
        health_check=get(data, 'health', '/api/health'),
        envs=data['envs']
    )
    template_path = f'/tmp/nomad/{service}-{group}.nomad'
    f = open(template_path, 'w+')
    f.write(output)
    f.close()
    if debug:
        print(output)

    script_path = exec.get_script_path(f'nomad.sh {template_path}')
    returncode, lines = exec.run(script_path, False)
    if returncode != 0:
        sys.exit(1)


def get(data: dict, key: str, default_value):
    if key in data:
        return data[key]
    else:
        return default_value








